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
        // BOTONES DEL HEADER
        addItemButton = new JButton("AGREGAR ITEM");
        menuButton = new JButton("COMPLETADOS"); // Inicia como "COMPLETADOS"
        exitButton = new JButton("SALIR");
        // PANEL PARA BOTONES DEL HEADER
        buttonPanel = new JPanel();
        buttonPanel.add(addItemButton);
        buttonPanel.add(menuButton); // Cambiamos el nombre del botón aquí
        buttonPanel.add(exitButton);
        // PANEL PARA ITEMS
        itemPanel = new JPanel();
        itemPanel.setLayout(new BoxLayout(itemPanel, BoxLayout.Y_AXIS));
        textArea = new JTextArea(5, 20);
        // CONFIGURACIÓN SIZE DEL FRAME
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        setSize(screenSize.width / 2, screenSize.height / 2);
        // CONFIGURAR LAYOUT
        getContentPane().setLayout(new BorderLayout());
        getContentPane().add(buttonPanel, BorderLayout.NORTH);
        getContentPane().add(new JScrollPane(itemPanel), BorderLayout.CENTER);
        getContentPane().add(new JScrollPane(textArea), BorderLayout.SOUTH);
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
            // CREAR PANEL DE BOTONES Y AGREGARLOS
            JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
            buttonPanel.add(deleteButton);
            buttonPanel.add(finishButton);
            itemRow.add(itemLabel, BorderLayout.WEST);
            itemRow.add(buttonPanel, BorderLayout.LINE_END);
            itemPanel.add(itemRow);
        }
        // VOLVER A VALIDAR Y REPAINT DE LA VISTA
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
            // CREAR PANEL DE BOTONES Y AGREGARLOS
            JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
            buttonPanel.add(deleteButton);
            itemRow.add(itemLabel, BorderLayout.WEST);
            itemRow.add(buttonPanel, BorderLayout.LINE_END);
            itemPanel.add(itemRow);
        }
        // VOLVER A VALIDAR Y REPAINT DE LA VISTA
        itemPanel.revalidate();
        itemPanel.repaint();
    }

    public String showInputDialog(String message) { return JOptionPane.showInputDialog(this, message); }

    public void limpiarTextArea() { textArea.setText(""); }

    public void mostrarError(String mensajeError) { JOptionPane.showMessageDialog(this, mensajeError); }

    public void cargarAgregarItemListener(ActionListener listener) { addItemButton.addActionListener(listener); }

    public void cargarMostrarCompletadosListener(ActionListener listener) { menuButton.addActionListener(listener); }

    public void cargarSalirListener(ActionListener listener) { exitButton.addActionListener(listener); }

    public void actualizarNombreBotonMenu(boolean enMenuPrincipal) {
        if (enMenuPrincipal) {
            menuButton.setText("COMPLETADOS");
        } else {
            menuButton.setText("MENU PRINCIPAL");
        }
    }

    public void ocultarAgregarItem(boolean ocultar) { addItemButton.setVisible(!ocultar); }
}
