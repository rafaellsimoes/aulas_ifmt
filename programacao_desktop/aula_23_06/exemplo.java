import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        JFrame frame = new JFrame("Consulta SIOPs");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 400);

        DefaultTableModel model = new DefaultTableModel();
        model.addColumn("Período");
        model.addColumn("Descrição");
        model.addColumn("Ano");

        JTable table = new JTable(model);
        JButton btnCarregar = new JButton("Carregar Dados");

        btnCarregar.addActionListener(e -> new Thread(() -> {
            try {
                URL url = new URL("https://siops-consulta-publica-api.saude.gov.br/v1/ano-periodo");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();

                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder json = new StringBuilder();
                String line;

                while ((line = reader.readLine()) != null) {
                    json.append(line);
                }

                List<String[]> dados = parseJsonManually(json.toString());
                SwingUtilities.invokeLater(() -> {
                    model.setRowCount(0);
                    for (String[] linha : dados) {
                        model.addRow(linha);
                    }
                });
            } catch (Exception ex) {
                ex.printStackTrace();
                JOptionPane.showMessageDialog(frame, "Erro: " + ex.getMessage());
            }
        }).start());

        frame.add(new JScrollPane(table), BorderLayout.CENTER);
        frame.add(btnCarregar, BorderLayout.SOUTH);
        frame.setVisible(true);
    }

    private static List<String[]> parseJsonManually(String json) {
        List<String[]> result = new ArrayList<>();
        // Remove colchetes e divide os objetos
        String content = json.substring(1, json.length() - 1);
        String[] objects = content.split("\\},\\s*\\{");

        for (String obj : objects) {
            obj = obj.replaceAll("[{}\"]", "");
            String[] fields = obj.split(",");

            String periodo = "", descricao = "", ano = "";

            for (String field : fields) {
                String[] keyValue = field.split(":");
                if (keyValue[0].trim().equals("nu_periodo")) {
                    periodo = keyValue[1].trim();
                } else if (keyValue[0].trim().equals("ds_periodo")) {
                    descricao = keyValue[1].trim();
                } else if (keyValue[0].trim().equals("ds_ano")) {
                    ano = keyValue[1].trim();
                }
            }

            result.add(new String[]{periodo, descricao, ano});
        }

        return result;
    }
}
