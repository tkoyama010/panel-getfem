import getfem as gf
import panel as pn
import pyvista as pv
from IPython.display import IFrame

pv.set_plot_theme("document")
pn.extension()

m = gf.Mesh("import", "gid", "tripod.GiD.msh")
m.export_to_vtk("tripod.vtk", "ascii")

mesh = pv.read("tripod.vtk")
plotter = pv.Plotter(notebook=True)
plotter.add_mesh(mesh)

def handler(viewer, src, **kwargs):
    return IFrame(src, "100%", "1000px")


iframe = plotter.show(
    jupyter_backend="trame",
    jupyter_kwargs=dict(handler=handler),
    return_viewer=True,
)

tabs = pn.Tabs(
    ("Mesh", pn.Spacer(styles=dict(background="red"), width=500, height=1000)),
    ("Model", pn.Spacer(styles=dict(background="blue"), width=500, height=1000)),
)

template = pn.template.MaterialTemplate(
    title='GetFEM',
    sidebar=[tabs],
    main=[pn.panel(iframe, width=1500, height=250)],
)

template.servable()
