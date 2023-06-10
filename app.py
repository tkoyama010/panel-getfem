import getfem as gf
import panel as pn
import param
import pyvista as pv
from IPython.display import IFrame

pv.set_plot_theme("document")
pn.extension()

title = pn.pane.Markdown("# panel-getfem")


class MeshVeiewer(param.Parameterized):
    mesh_name = param.ObjectSelector(
        default="tripod.mesh",
        objects=[
            "tripod.mesh",
        ],
    )
    plotter = pv.Plotter(notebook=True)

    def handler(self, viewer, src, **kwargs):
        return IFrame(src, "100%", "1000px")

    @param.depends("mesh_name")
    def view(self):
        m = gf.Mesh("load", self.mesh_name)
        m.export_to_vtk(str(id(self)) + ".vtk", "ascii")
        mesh = pv.read(str(id(self)) + ".vtk")

        self.plotter.clear()
        self.plotter.add_mesh(mesh)
        iframe = self.plotter.show(
            jupyter_backend="trame",
            jupyter_kwargs=dict(handler=self.handler),
            return_viewer=True,
        )
        return iframe


class ResultVeiewer(param.Parameterized):
    result_name = param.ObjectSelector(
        default="tripod.vtk",
        objects=[
            "tripod.vtk",
        ],
    )
    plotter = pv.Plotter(notebook=True)

    def handler(self, viewer, src, **kwargs):
        return IFrame(src, "100%", "1000px")

    @param.depends("result_name")
    def view(self):
        result = pv.read(self.result_name)

        self.plotter.clear()
        self.plotter.add_mesh(result)
        iframe = self.plotter.show(
            jupyter_backend="trame",
            jupyter_kwargs=dict(handler=self.handler),
            return_viewer=True,
        )
        return iframe


mesh_viewer = MeshVeiewer(name="Mesh Viewer")
result_viewer = ResultVeiewer(name="Result Viewer")

pn.Column(
    title,
    pn.Tabs(
        (
            "Mesh",
            pn.Row(
                mesh_viewer.param, pn.panel(mesh_viewer.view, width=1000, height=250)
            ),
        ),
        ("Fem", pn.Spacer(styles=dict(background="red"), width=500, height=1000)),
        ("Integ", pn.Spacer(styles=dict(background="blue"), width=500, height=1000)),
        ("Model", pn.Spacer(styles=dict(background="yellow"), width=500, height=1000)),
        (
            "Result",
            pn.Row(
                result_viewer.param,
                pn.panel(result_viewer.view, width=1000, height=250),
            ),
        ),
    ),
).show()
