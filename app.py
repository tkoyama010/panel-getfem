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
    def view(self, plotter):
        m = gf.Mesh("load", self.file_name)
        m.export_to_vtk(str(id(self)) + ".vtk", "ascii")
        return plotter.view(str(id(self)) + ".vtk")


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


class Plotter(param.Parameterized):
    plotter = pv.Plotter(notebook=True)

    def handler(self, viewer, src, **kwargs):
        return IFrame(src, "100%", "1000px")

    def view(self, file_name):
        mesh = pv.read(file_name)
        self.plotter.clear()
        self.plotter.add_mesh(mesh)
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
plotter = Plotter(name="Plotter")

pn.Row(
    pn.Tabs(
        (
            "Model",
            pn.Column(mesh.param, fem.param, integ.param, model.param),
        ),
        (
            "Plotter",
            pn.Row(
                plotter.param,
            ),
        ),
    ),
    pn.panel(mesh.view(plotter), width=1000, height=250),
).show()
