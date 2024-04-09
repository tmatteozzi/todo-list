import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;
import java.util.ArrayList;

public class ToDoListView extends JFrame {
    private JPanel buttonPanel, itemPanel;
    private JButton menuButton, addItemButton, exitButton;
    private JTextArea textArea;

    public ToDoListView() {
        // CONFIGURACIÓN INTERFAZ FRAME
        setTitle("TO DO LIST");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        addItemButton = new JButton("AGREGAR ITEM");
        menuButton = new JButton("COMPLETADOS"); // Inicia como "COMPLETADOS"
        exitButton = new JButton("SALIR");

        buttonPanel = new JPanel();
        buttonPanel.add(addItemButton);
        buttonPanel.add(menuButton); // Cambiamos el nombre del botón aquí
        buttonPanel.add(exitButton);

        itemPanel = new JPanel();
        itemPanel.setLayout(new BoxLayout(itemPanel, BoxLayout.Y_AXIS));
        textArea = new JTextArea(5, 20);

        // Obtener el tamaño de la pantalla
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        int screenWidth = screenSize.width;
        int screenHeight = screenSize.height;
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

    public void updateUnfinished(ArrayList<Item> itemList) {
        itemPanel.removeAll();
        for (Item item : itemList) {
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
            buttonPanel.add(finishButton);
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

    public void updateCompleted(ArrayList<Item> itemList) {
        itemPanel.removeAll();
        for (Item item : itemList) {
            // CREAR PANEL PARA EL ITEM
            JPanel itemRow = new JPanel();
            itemRow.setLayout(new BorderLayout());
            JLabel itemLabel = new JLabel(item.getDescription());
            itemRow.setPreferredSize(new Dimension(itemRow.getPreferredSize().width, 50));

            // BOTÓN ELIMINAR
            JButton deleteButton = new JButton("ELIMINAR");

            // Crear un panel para los botones y establecer su diseño como FlowLayout con alineación a la derecha
            JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));

            // Añadir el botón al panel de botones
            buttonPanel.add(deleteButton);
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
        menuButton.addActionListener(listener);
    }

    public void cargarSalirListener(ActionListener listener) {
        exitButton.addActionListener(listener);
    }

    public void cargarEliminarItemListener(ActionListener listener) {
        for (Component component : itemPanel.getComponents()) {
            if (component instanceof JPanel) {
                JPanel itemRow = (JPanel) component;
                for (Component comp : itemRow.getComponents()) {
                    if (comp instanceof JPanel) {
                        JPanel buttonPanel = (JPanel) comp;
                        for (Component btnComp : buttonPanel.getComponents()) {
                            if (btnComp instanceof JButton) {
                                JButton deleteButton = (JButton) btnComp;
                                if (deleteButton.getText().equals("ELIMINAR")) {
                                    deleteButton.addActionListener(listener);
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    public void actualizarNombreBotonMenu(boolean enMenuPrincipal) {
        if (enMenuPrincipal) {
            menuButton.setText("COMPLETADOS");
        } else {
            menuButton.setText("MENU PRINCIPAL");
        }
    }

    public void ocultarAgregarItem(boolean ocultar) {
        addItemButton.setVisible(!ocultar);
    }
}
