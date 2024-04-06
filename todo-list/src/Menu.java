import javax.swing.*;
import java.awt.*;
import java.util.List;

public class Menu extends JFrame {
    // ATTRIBUTES
    private ToDoList todoList;
    private JPanel buttonPanel, itemPanel, itemRow;
    private JButton showCompletedButton, addItemButton, exitButton, deleteItemButton, finishItemButton;
    private JLabel itemLabel;
    private JTextArea textArea;
    private JScrollPane scrollPane;
    private boolean showingCompleted = false;
    private List<Item> items;

    public Menu() {
        todoList = new ToDoList();
        crearGui();
        updateList();
    }

    public void crearGui() {
        // MAIN CONFIG
        setTitle("TO DO LIST");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // BUTTONS
        addItemButton = new JButton("ADD ITEM");
        showCompletedButton = new JButton("FINISHED");
        exitButton = new JButton("EXIT");

        // BUTTON PANEL
        buttonPanel = new JPanel();
        buttonPanel.add(addItemButton);
        buttonPanel.add(showCompletedButton);
        buttonPanel.add(exitButton);

        // ACTION LISTENERS
        addItemButton.addActionListener(e -> {
            textArea = new JTextArea(5, 20);
            scrollPane = new JScrollPane(textArea);
            // RESULT CONFIG
            int result = JOptionPane.showOptionDialog(
                    null,
                    scrollPane,
                    "DESCRIPTION:",
                    JOptionPane.OK_CANCEL_OPTION,
                    JOptionPane.PLAIN_MESSAGE,
                    null,
                    null,
                    null
            );
            // RESULT VALIDATION
            if (result == JOptionPane.OK_OPTION) {
                String description = textArea.getText();
                // IF THE ITEM DESC ALREADY EXIST DON'T ADD
                boolean duplicate = todoList.getAllItems().stream().anyMatch(item -> item.getDescription().equals(description));
                if (!duplicate) {
                    todoList.addItem(new Item(description));
                    updateList();
                } else {
                    JOptionPane.showMessageDialog(null, "AN ITEM WITH THE SAME DESCRIPTION ALREADY EXISTS.", "ERROR", JOptionPane.ERROR_MESSAGE);
                }
            }
        });

        showCompletedButton.addActionListener(e -> {
            if (!showingCompleted) {
                showCompleted();
            } else {
                mainMenu();
            }
        });

        exitButton.addActionListener(e -> System.exit(0));

        // ITEM LIST PANEL
        itemPanel = new JPanel();
        itemPanel.setLayout(new BoxLayout(itemPanel, BoxLayout.Y_AXIS));

        // ADD ELEMENTS TO MAIN LAYOUT
        getContentPane().setLayout(new BorderLayout());
        getContentPane().add(buttonPanel, BorderLayout.NORTH);
        getContentPane().add(new JScrollPane(itemPanel), BorderLayout.CENTER);
        pack();
        setLocationRelativeTo(null);
        setVisible(true);
    }

    // METHOD TO UPDATE EACH TIME A CHANGE IS MADE
    public void updateList() {
        // EMPTY THE ITEM PANEL
        itemPanel.removeAll();
        items = todoList.getAllItems();
        for (Item item : items) {
            if (!item.isDone()) {  // ONLY SHOW NON-FINISHED ITEMS
                itemRow = new JPanel();
                itemRow.setLayout(new BorderLayout());
                itemLabel = new JLabel(item.getDescription());
                // FINISH THE TASK
                finishItemButton = new JButton("DONE");
                finishItemButton.addActionListener(e -> {
                    todoList.finishItem(item);
                    updateList(); // RECURSIVELY DO EVERYTHING AGAIN ONCE THE BUTTON IS PRESSED
                });
                // ADD ROWS TO ITEM PANEL
                itemRow.add(itemLabel, BorderLayout.WEST);
                itemRow.add(finishItemButton, BorderLayout.EAST);
                itemPanel.add(itemRow);
            }
        }
        // REMAKE CHANGES
        itemPanel.revalidate();
        itemPanel.repaint();
    }


    public void showCompleted() {
        addItemButton.setVisible(false);
        // EMPTY THE ITEM PANEL
        itemPanel.removeAll();
        items = todoList.getAllItems();
        for (Item item : items) {
            if (item.isDone()) { // ONLY SHOW FINISHED ITEMS
                itemRow = new JPanel();
                itemRow.setLayout(new BorderLayout());
                // SHOW DESC + DATE
                itemLabel = new JLabel(item.getDescription() + " - " + item.getDate());
                // DELETE OPTION
                deleteItemButton = new JButton("DELETE");
                deleteItemButton.addActionListener(e -> {
                    todoList.deleteItem(item);
                    showCompleted();
                });
                // ADD ROWS TO ITEM PANEL
                itemRow.add(itemLabel, BorderLayout.WEST);
                itemRow.add(deleteItemButton, BorderLayout.EAST);
                itemPanel.add(itemRow);
            }
        }
        // REMAKE CHANGES
        itemPanel.revalidate();
        itemPanel.repaint();
        // CHANGE BUTTON TO MAIN MENU
        showCompletedButton.setText("MAIN MENU");
        showingCompleted = true;
    }

    public void mainMenu() { // UPDATE MAIN LIST AND CHANGE BUTTON TEXT
        addItemButton.setVisible(true);
        updateList();
        showCompletedButton.setText("FINISHED");
        showingCompleted = false;
    }
}
