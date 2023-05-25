import panel as pn

pn.extension()

tabs = pn.Tabs(
    ("red", pn.Spacer(styles=dict(background="red"), width=500, height=1000)),
    ("blue", pn.Spacer(styles=dict(background="blue"), width=500, height=1000)),
    ("green", pn.Spacer(styles=dict(background="green"), width=500, height=1000)),
)

pn.Row(
    tabs,
).show()
