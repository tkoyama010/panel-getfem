import os

import getfem as gf
import panel as pn
import pyvista as pv
from IPython.display import IFrame

pv.set_plot_theme("document")
pn.extension()

file_name = os.path.join(os.path.dirname(__file__), "tripod.GiD.msh")
m = gf.Mesh("import", "gid", file_name)
m.export_to_vtk("tripod.vtk", "ascii")

mesh = pv.read("tripod.vtk")
plotter = pv.Plotter(notebook=True)
plotter.add_mesh(mesh)

def handler(viewer, src, **kwargs):
    return IFrame(src, "100%", "1000px")

file_input = pn.widgets.FileInput()

iframe = plotter.show(
    jupyter_backend="trame",
    jupyter_kwargs=dict(handler=handler),
    return_viewer=True,
)

tabs = pn.Tabs(
    ("Mesh", file_input),
    ("Model", pn.Spacer(styles=dict(background="blue"), width=500, height=1000)),
)

template = pn.template.MaterialTemplate(
    title='GetFEM',
    sidebar=[tabs],
    main=[pn.panel(iframe, width=1500, height=250)],
)

template.servable()
