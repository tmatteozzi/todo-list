import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;
import java.util.ArrayList;

public class ToDoListView extends JFrame {
    private JPanel buttonPanel, itemPanel;
    private JButton showCompletedButton, addItemButton, exitButton;
    private JTextArea textArea;
    private JScrollPane scrollPane;
    private ToDoListModel model;
    private boolean showFinishButton = true;

    public ToDoListView(ToDoListModel model) {
        this.model = model;
        setTitle("TO DO LIST");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        addItemButton = new JButton("AGREGAR ITEM");
        showCompletedButton = new JButton("COMPLETADOS");
        exitButton = new JButton("SALIR");

        buttonPanel = new JPanel();
        buttonPanel.add(addItemButton);
        buttonPanel.add(showCompletedButton);
        buttonPanel.add(exitButton);

        itemPanel = new JPanel();
        itemPanel.setLayout(new BoxLayout(itemPanel, BoxLayout.Y_AXIS));

        textArea = new JTextArea(5, 20);
        scrollPane = new JScrollPane(textArea);

        getContentPane().setLayout(new BorderLayout());
        getContentPane().add(buttonPanel, BorderLayout.NORTH);
        getContentPane().add(new JScrollPane(itemPanel), BorderLayout.CENTER);
        getContentPane().add(scrollPane, BorderLayout.SOUTH);
        pack();
        setLocationRelativeTo(null);
        setVisible(true);
    }

    public void updateList(ArrayList<Item> itemList, boolean showCompleted) {
        itemPanel.removeAll();
        for (Item item : itemList) {
            if (showCompleted && !item.isDone()) {
                continue; // Si se quiere mostrar completados y este ítem no está completado, saltarlo
            }
            if (!showCompleted && item.isDone()) {
                continue; // Si no se quiere mostrar completados y este ítem está completado, saltarlo
            }

            JPanel itemRow = new JPanel();
            itemRow.setLayout(new BorderLayout());

            JLabel itemLabel = new JLabel(item.getDescription());

            if (showFinishButton) {
                JButton finishButton = new JButton("Finalizar");
                finishButton.addActionListener(e -> {
                    model.finishItem(item);
                    updateList(model.getUnfinishedItems(), showCompleted);
                });
                itemRow.add(finishButton, BorderLayout.EAST);
            }

            JButton deleteButton = new JButton("Eliminar");
            deleteButton.addActionListener(e -> {
                model.deleteItem(item);
                updateList(model.getAllItems(), showCompleted);
            });

            itemRow.add(itemLabel, BorderLayout.CENTER);
            itemRow.add(deleteButton, BorderLayout.WEST);

            itemPanel.add(itemRow);
        }

        itemPanel.revalidate();
        itemPanel.repaint();
    }

    public String showInputDialog(String message) {
        return JOptionPane.showInputDialog(this, message);
    }

    public void limpiarTextArea() {
        textArea.setText("");
    }

    public void mostrarError(String mensajeError) {
        JOptionPane.showMessageDialog(this, mensajeError);
    }

    public void cargarAgregarItemListener(ActionListener listener) {
        addItemButton.addActionListener(listener);
    }

    public void cargarMostrarCompletadosListener(ActionListener listener) {
        showCompletedButton.addActionListener(listener);
    }

    public void cargarSalirListener(ActionListener listener) {
        exitButton.addActionListener(listener);
    }

    // Método para ocultar o mostrar el botón de agregar ítem y transformar el botón de completados en menú principal
    public void transformarEnMenuPrincipal(boolean ocultarAgregarItem) {
        if (ocultarAgregarItem) {
            buttonPanel.remove(addItemButton);
        } else {
            buttonPanel.add(addItemButton);
        }
        showCompletedButton.setText("COMPLETADOS");
        showCompletedButton.addActionListener(e -> {
            if (!ocultarAgregarItem) {
                buttonPanel.add(addItemButton);
            }
            showCompletedButton.setText("COMPLETADOS");
            updateList(model.getAllItems(), false); // Mostrar todos los ítems nuevamente al regresar al menú principal
        });
        buttonPanel.revalidate();
        buttonPanel.repaint();
    }
}
