import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class ToDoListController {
    private ToDoListView view;
    private ToDoListModel model;
    private boolean enMenuPrincipal = false;

    public ToDoListController(ToDoListView view, ToDoListModel model) {
        this.view = view;
        this.model = model;

        view.updateList(model.getUnfinishedItems(), false); // Mostrar solo los ítems no completados al inicio
        view.cargarAgregarItemListener(new AgregarItemListener());
        view.cargarMostrarCompletadosListener(new MostrarCompletadosListener());
        view.cargarSalirListener(new SalirListener());
    }

    class AgregarItemListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            String description = view.showInputDialog("Ingrese la descripción del nuevo ítem:");
            if (description != null && !description.isEmpty()) {
                model.addItem(new Item(description));
                actualizarLista();
                view.limpiarTextArea();
            } else {
                view.mostrarError("El campo de descripción está vacío.");
            }
        }
    }

    class MostrarCompletadosListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            if (enMenuPrincipal) {
                enMenuPrincipal = false;
                actualizarLista(); // Mostrar todos los ítems nuevamente al regresar al menú principal
                view.transformarEnMenuPrincipal(false); // Transformar el botón de completados en menú principal
                view.setShowFinishButton(true); // Mostrar botón "Finalizar" en la lista de ítems
            } else {
                view.updateList(model.getCompletedItems(), true); // Mostrar solo los ítems completados
                view.transformarEnMenuPrincipal(true); // Transformar el botón de completados en menú principal
                view.setShowFinishButton(false); // Ocultar botón "Finalizar" en la lista de ítems
                enMenuPrincipal = true;
            }
        }
    }

    class SalirListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            System.exit(0);
        }
    }

    // Método para actualizar la lista después de realizar operaciones de edición
    public void actualizarLista() {
        view.updateList(model.getAllItems(), false); // Actualizar la lista mostrando todos los ítems
    }

    // Método para indicar que se está en el menú principal
    public void setEnMenuPrincipal(boolean enMenuPrincipal) {
        this.enMenuPrincipal = enMenuPrincipal;
    }
}
