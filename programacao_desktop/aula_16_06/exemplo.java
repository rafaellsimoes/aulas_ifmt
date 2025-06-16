
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class App {

    public static void main(String[] args) {
        try {
            String apiUrl = "https://siops-consulta-publica-api.saude.gov.br/v1/ano-periodo";
            String jsonResponse = getApiData(apiUrl);
            System.out.println("Dados da API:");
            System.out.println(jsonResponse);
        } catch (Exception e) {
            System.err.println("Erro ao acessar a API: " + e.getMessage());
        }
    }

    public static String getApiData(String apiUrl) throws Exception {
        URL url = new URL(apiUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();

        // Configura a requisição
        connection.setRequestMethod("GET");
        connection.setRequestProperty("Accept", "application/json");

        // Verifica se a resposta foi bem sucedida
        if (connection.getResponseCode() != 200) {
            throw new RuntimeException("Falha na requisição: HTTP " + connection.getResponseCode());
        }

        // Lê a resposta
        BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        StringBuilder response = new StringBuilder();
        String line;

        while ((line = reader.readLine()) != null) {
            response.append(line);
        }

        // Fecha as conexões
        reader.close();
        connection.disconnect();

        return response.toString();
    }
}
