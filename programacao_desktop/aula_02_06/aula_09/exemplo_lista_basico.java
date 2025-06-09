import java.util.ArrayList;
import java.util.List;

public class ExemploList {
    public static void main(String[] args) {

        List<String> frutas = new ArrayList<>();
        
        frutas.add("Maçã");
        frutas.add("Banana");
        frutas.add("Laranja");
        frutas.add("Banana"); 
        
        System.out.println("Lista de frutas: " + frutas);
        
        System.out.println("Segunda fruta: " + frutas.get(1));
    
        frutas.remove("Banana"); 
        System.out.println("Após remover Banana: " + frutas);

        List<Double> numeros = new ArrayList<>();

        numeros.add(1.0);
        numeros.add(2.45);
        numeros.add(46.48);
        numeros.add(78.0);
        System.out.println("Lista de Números : " + numeros);    
        System.out.println("Segunda fruta: " + numeros.get(2));

    }
}
