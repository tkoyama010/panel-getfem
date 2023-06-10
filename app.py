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


class Model(param.Parameterized):
    brick_name = param.ObjectSelector(
        default="linearized elasticity brick",
        objects=[
            "linearized elasticity brick",
        ],
    )


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
        solution = pv.read(self.file_name)

        self.plotter.clear()
        self.plotter.add_mesh(solution)
        iframe = self.plotter.show(
            jupyter_backend="trame",
            jupyter_kwargs=dict(handler=self.handler),
            return_viewer=True,
        )
        return iframe


mesh = Mesh(name="Mesh")
fem = Fem(name="Fem")
integ = Integ(name="Integ")
model = Model(name="Model")
solution = Solution(name="Solution")

pn.Column(
    title,
    pn.Tabs(
        (
            "Model",
            pn.Row(
                pn.Column(mesh.param, fem.param, integ.param, model.param),
                pn.panel(mesh.view, width=1000, height=250),
            ),
        ),
        (
            "Solution",
            pn.Row(
                solution.param,
                pn.panel(solution.view, width=1000, height=250),
            ),
        ),
    ),
).show()
