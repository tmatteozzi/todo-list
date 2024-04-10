import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class ToDoListController {
    private ToDoListView view;
    private ToDoListModel model;
    private boolean enMenuPrincipal = true;

    public ToDoListController(ToDoListView view, ToDoListModel model) {
        this.view = view;
        this.model = model;

        // CARGAR LISTENERS
        view.cargarAgregarItemListener(new AgregarItemListener());
        view.cargarMostrarCompletadosListener(new MostrarCompletadosListener());
        view.cargarSalirListener(new SalirListener());

        // MOSTRAR MENU PRINCIPAL AL INICIO & CONFIGURACIÓN INICIAL
        view.updateUnfinished(model.getUnfinishedItems());
        view.actualizarNombreBotonMenu(enMenuPrincipal);
        view.ocultarAgregarItem(!enMenuPrincipal);
    }

    class AgregarItemListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            String description = view.showInputDialog("Ingrese la descripción del nuevo ítem:");
            if (description != null && !description.isEmpty()) {
                model.addItem(new Item(description));
                if (enMenuPrincipal) {
                    view.updateUnfinished(model.getUnfinishedItems());
                } else {
                    view.updateCompleted(model.getCompletedItems());
                }
                view.limpiarTextArea();
            } else {
                view.mostrarError("El campo de descripción está vacío.");
            }
        }
    }

    class MostrarCompletadosListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            if (enMenuPrincipal) {
                view.updateCompleted(model.getCompletedItems());
            } else {
                view.updateUnfinished(model.getUnfinishedItems());
            }
            enMenuPrincipal = !enMenuPrincipal;
            view.actualizarNombreBotonMenu(enMenuPrincipal);
            view.ocultarAgregarItem(!enMenuPrincipal);
        }
    }

    class SalirListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            System.exit(0);
        }
    }
}
