import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;
import java.util.ArrayList;

public class ToDoListView extends JFrame {
    private JPanel buttonPanel, itemPanel;
    private JButton CompletedButton, addItemButton, exitButton;
    private JTextArea textArea;

    public ToDoListView() {
        setTitle("TO DO LIST");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        addItemButton = new JButton("AGREGAR ITEM");
        CompletedButton = new JButton("COMPLETADOS");
        exitButton = new JButton("SALIR");

        buttonPanel = new JPanel();
        buttonPanel.add(addItemButton);
        buttonPanel.add(CompletedButton);
        buttonPanel.add(exitButton);

        itemPanel = new JPanel();
        itemPanel.setLayout(new BoxLayout(itemPanel, BoxLayout.Y_AXIS));

        textArea = new JTextArea(5, 20);

        // Obtener el tamaño de la pantalla
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        int screenWidth = screenSize.width;
        int screenHeight = screenSize.height;

        // Establecer el tamaño del JFrame al 50% de la pantalla
        setSize(screenWidth / 2, screenHeight / 2);

        // Configurar el layout del JFrame
        getContentPane().setLayout(new BorderLayout());
        getContentPane().add(buttonPanel, BorderLayout.NORTH);
        getContentPane().add(new JScrollPane(itemPanel), BorderLayout.CENTER);
        getContentPane().add(new JScrollPane(textArea), BorderLayout.SOUTH);

        // Hacer visible el JFrame
        setLocationRelativeTo(null);
        setVisible(true);
    }

    public void updateList(ArrayList<Item> itemList, boolean showCompleted, boolean enMenuPrincipal) {
        itemPanel.removeAll();
        for (Item item : itemList) {
            // Si se quiere mostrar completados y el ítem no está completado, o viceversa, saltar al siguiente ítem
            if ((showCompleted && !item.isDone()) || (!showCompleted && item.isDone())) {
                continue;
            }

            // CREAR PANEL PARA EL ITEM
            JPanel itemRow = new JPanel();
            itemRow.setLayout(new BorderLayout());
            JLabel itemLabel = new JLabel(item.getDescription());
            itemRow.setPreferredSize(new Dimension(itemRow.getPreferredSize().width, 50));

            // BOTONES
            JButton finishButton = new JButton("FINALIZAR");
            JButton deleteButton = new JButton("ELIMINAR");

            // Crear un panel para los botones y establecer su diseño como FlowLayout con alineación a la derecha
            JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));

            // Añadir los botones al panel de botones
            buttonPanel.add(deleteButton);
            if (!enMenuPrincipal) {
                buttonPanel.add(finishButton);
            }
            itemRow.add(itemLabel, BorderLayout.WEST);
            // Añadir el panel de botones al panel de ítem
            itemRow.add(buttonPanel, BorderLayout.LINE_END);

            // Añadir el panel del ítem al panel principal
            itemPanel.add(itemRow);
        }

        // Volver a validar el panel de ítems y repintar la vista
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
        CompletedButton.addActionListener(listener);
    }

    public void cargarSalirListener(ActionListener listener) {
        exitButton.addActionListener(listener);
    }

    // Método para ocultar o mostrar el botón de agregar ítem y transformar el botón de completados en menú principal
    public void transformarEnMenuPrincipal(boolean ocultarAgregarItem, boolean enMenuPrincipal) {
        addItemButton.setVisible(!ocultarAgregarItem);
        CompletedButton.addActionListener(e -> {
            if (!ocultarAgregarItem) {
                addItemButton.setVisible(true);
            }
            CompletedButton.setText(enMenuPrincipal ? "COMPLETADOS" : "MENU PRINCIPAL");
            // Implementa esta lógica según tus necesidades
        });
        buttonPanel.revalidate();
        buttonPanel.repaint();
    }
}
