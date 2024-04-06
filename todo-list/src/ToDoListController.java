import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class ToDoListController {
    private ToDoListView view;
    private ToDoListModel model;
    private boolean enMenuPrincipal = false;

    public ToDoListController(ToDoListView view, ToDoListModel model) {
        this.view = view;
        this.model = model;

        view.updateList(model.getUnfinishedItems(), false);
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
                actualizarLista();
                view.transformarEnMenuPrincipal(false); 
            } else {
                view.updateList(model.getCompletedItems(), true);
                view.transformarEnMenuPrincipal(true);
                enMenuPrincipal = true;
            }
        }
    }

    class SalirListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            System.exit(0);
        }
    }

    public void actualizarLista() {
        view.updateList(model.getAllItems(), false);
    }

    public void setEnMenuPrincipal(boolean enMenuPrincipal) {
        this.enMenuPrincipal = enMenuPrincipal;
    }
}
