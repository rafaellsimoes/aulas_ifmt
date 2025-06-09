import java.util.ArrayList;
import java.util.List;

public class ExemploList {
    public static void main(String[] args) {
        // Criando uma List (ArrayList)
        List<String> frutas = new ArrayList<>();
        
        // Adicionando elementos
        frutas.add("Maçã");
        frutas.add("Banana");
        frutas.add("Laranja");
        frutas.add("Banana"); // List permite elementos duplicados
        
        // Imprimindo a lista
        System.out.println("Lista de frutas: " + frutas);
        
        // Acessando um elemento pelo índice
        System.out.println("Segunda fruta: " + frutas.get(1));
        
        // Removendo um elemento
        frutas.remove("Banana"); // Remove a primeira ocorrência
        System.out.println("Após remover Banana: " + frutas);
    }
}
