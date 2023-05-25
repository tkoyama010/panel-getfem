import panel as pn

pn.extension()

tabs = pn.Tabs(
    ("Mesher", pn.Spacer(styles=dict(background="red"), width=500, height=1000)),
    ("Mesh", pn.Spacer(styles=dict(background="blue"), width=500, height=1000)),
    ("Fem", pn.Spacer(styles=dict(background="green"), width=500, height=1000)),
    ("Integ", pn.Spacer(styles=dict(background="red"), width=500, height=1000)),
    ("Model", pn.Spacer(styles=dict(background="blue"), width=500, height=1000)),
)

pn.Row(
    tabs,
).show()
