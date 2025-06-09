import java.util.HashSet;
import java.util.Set;

public class ExemploSet {
    public static void main(String[] args) {
        // Criando um Set (HashSet)
        Set<String> carros = new HashSet<>();
        
        // Adicionando elementos
        carros.add("Fusca");
        carros.add("Gol");
        carros.add("Palio");
        carros.add("Gol"); // Set não permite elementos duplicados (ignorado)
        
        // Imprimindo o conjunto
        System.out.println("Conjunto de carros: " + carros);
        
        // Verificando se um elemento existe
        System.out.println("Tem Fusca? " + carros.contains("Fusca"));
        
        // Removendo um elemento
        carros.remove("Palio");
        System.out.println("Após remover Palio: " + carros);
    }
}
