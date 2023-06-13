import panel as pn
import param

pn.extension()


class Model(param.Parameterized):

    brick_list = param.List([])
    brick = param.String()

    def _add_brick(self):
        if len(self.brick) > 0:
            brick = Brick(parent=self, args=self.brick, name="")
            brick.param.watch(self._delete, ["delete"])
            self.brick_list.append(brick)
            self.param.trigger("brick_list")
            self.brick = ""

    add_brick = param.Action(_add_brick)

    def _delete(self, *events):
        for event in events:
            if event.name == "delete":
                self.brick_list.remove(event.obj)
                self.param.trigger("brick_list")


class Brick(param.Parameterized):

    delete = param.Event()
    args = ""


model = Model()


@pn.depends(model.param.brick_list)
def brick_list(brick_list):
    message = lambda x: pn.pane.Markdown("### " + x, width=200)
    delete = lambda x: pn.Param(
        x,
        widgets={
            "delete": {
                "widget_type": pn.widgets.Button,
                "button_type": "danger",
                "name": "x",
                "width": 15,
            }
        },
    )
    return pn.Column(
        *[
            pn.Row(message(brick.args), delete(brick.param.delete))
            for brick in brick_list
        ]
    )


pn.Column(
    pn.pane.Markdown("## Model"),
    pn.Row(
        pn.Param(
            model.param.brick,
            widgets={
                "brick": {
                    "widget_type": pn.widgets.TextInput,
                    "name": "",
                    "placeholder": "Enter a Brick...",
                }
            },
        ),
        pn.Param(
            model.param.add_brick,
            widgets={
                "add_brick": {
                    "widget_type": pn.widgets.Button,
                    "button_type": "primary",
                    "name": "+",
                    "width": 15,
                }
            },
        ),
    ),
    brick_list,
).servable()
