import getfem as gf
import panel as pn
import param
import pyvista as pv
from IPython.display import IFrame

pv.set_plot_theme("document")
pn.extension()


class Mesh(param.Parameterized):
    file_name = param.ObjectSelector(
        default="tripod.mesh",
        objects=[
            "tripod.mesh",
        ],
    )

    @param.depends("file_name")
    def show(self, plotter):
        m = gf.Mesh("load", self.file_name)
        m.export_to_vtk(str(id(self)) + ".vtk", "ascii")
        return plotter.show(str(id(self)) + ".vtk")


class Fem(param.Parameterized):
    file_name = param.ObjectSelector(
        default="tripod.mfu",
        objects=[
            "tripod.mfu",
            "tripod.mfue",
        ],
    )


class Integ(param.Parameterized):
    file_name = param.ObjectSelector(
        default="tripod.mim",
        objects=[
            "tripod.mim",
        ],
    )


class Plotter(param.Parameterized):
    plotter = pv.Plotter(notebook=True)

    def handler(self, viewer, src, **kwargs):
        return IFrame(src, "100%", "1000px")

    def show(self, file_name):
        mesh = pv.read(file_name)
        self.plotter.clear()
        self.plotter.add_mesh(mesh)
        iframe = self.plotter.show(
            jupyter_backend="trame",
            jupyter_kwargs=dict(handler=self.handler),
            return_viewer=True,
        )
        return iframe


text = pn.widgets.TextInput(value="Ready")
button = pn.widgets.Button(name="Click me", button_type="primary")


def add_brick(event):
    text.value = "Clicked {0} times".format(button.clicks)


button.on_click(add_brick)


mesh = Mesh(name="Mesh")
fem = Fem(name="Fem")
integ = Integ(name="Integ")
plotter = Plotter(name="Plotter")

pn.Row(
    pn.Tabs(
        (
            "Model",
            pn.Column(
                mesh.param, fem.param, integ.param, pn.Row(button, text)
            ),
        ),
        (
            "Plotter",
            pn.Row(
                plotter.param,
            ),
        ),
    ),
    pn.panel(mesh.show(plotter), width=1000, height=250),
).show()
