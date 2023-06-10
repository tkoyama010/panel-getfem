import getfem as gf
import panel as pn
import param
import pyvista as pv
from IPython.display import IFrame

pv.set_plot_theme("document")
pn.extension()

title = pn.pane.Markdown("# panel-getfem")


class Mesh(param.Parameterized):
    file_name = param.ObjectSelector(
        default="tripod.mesh",
        objects=[
            "tripod.mesh",
        ],
    )
    plotter = pv.Plotter(notebook=True)

    def handler(self, viewer, src, **kwargs):
        return IFrame(src, "100%", "1000px")

    @param.depends("file_name")
    def view(self):
        m = gf.Mesh("load", self.file_name)
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

class Fem(param.Parameterized):
    pass

class Integ(param.Parameterized):
    pass

class Model(param.Parameterized):
    pass


class Solution(param.Parameterized):
    file_name = param.ObjectSelector(
        default="tripod.vtk",
        objects=[
            "tripod.vtk",
        ],
    )
    plotter = pv.Plotter(notebook=True)

    def handler(self, viewer, src, **kwargs):
        return IFrame(src, "100%", "1000px")

    @param.depends("file_name")
    def view(self):
        result = pv.read(self.file_name)

        self.plotter.clear()
        self.plotter.add_mesh(result)
        iframe = self.plotter.show(
            jupyter_backend="trame",
            jupyter_kwargs=dict(handler=self.handler),
            return_viewer=True,
        )
        return iframe


mesh = Mesh(name="Mesh")
result = Solution(name="Solution")

pn.Column(
    title,
    pn.Tabs(
        (
            "Mesh",
            pn.Row(
                mesh.param, pn.panel(mesh.view, width=1000, height=250)
            ),
        ),
        ("Fem", pn.Spacer(styles=dict(background="red"), width=500, height=1000)),
        ("Integ", pn.Spacer(styles=dict(background="blue"), width=500, height=1000)),
        ("Model", pn.Spacer(styles=dict(background="yellow"), width=500, height=1000)),
        (
            "Solution",
            pn.Row(
                result.param,
                pn.panel(result.view, width=1000, height=250),
            ),
        ),
    ),
).show()
