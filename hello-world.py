import panel as pn

pn.extension()

tabs = pn.Tabs(
    ("red", pn.Spacer(styles=dict(background="red"), width=100, height=100)),
    ("blue", pn.Spacer(styles=dict(background="blue"), width=100, height=100)),
    ("green", pn.Spacer(styles=dict(background="green"), width=100, height=100)),
    closable=True,
)

pn.Row(
    tabs,
    tabs.clone(active=1, tabs_location="right"),
    tabs.clone(active=2, tabs_location="below"),
    tabs.clone(tabs_location="left"),
).show()
