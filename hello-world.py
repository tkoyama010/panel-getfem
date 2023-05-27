import getfem as gf
import panel as pn
import pyvista as pv
from IPython.display import IFrame

pv.set_plot_theme("document")
pn.extension()

m = gf.Mesh("import", "gid", "tripod.GiD.msh")

tabs = pn.Tabs(
    ("Mesh", pn.Spacer(styles=dict(background="blue"), width=500, height=1000)),
    ("Model", pn.Spacer(styles=dict(background="blue"), width=500, height=1000)),
)

pn.Row(
    tabs,
).show()
