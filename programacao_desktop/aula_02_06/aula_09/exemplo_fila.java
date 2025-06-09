import java.util.LinkedList;
import java.util.Queue;

public class ExemploQueue {
    public static void main(String[] args) {
        // Criando uma Queue (LinkedList)
        Queue<String> fila = new LinkedList<>();
        
        // Adicionando elementos (enqueue)
        fila.add("Primeiro");
        fila.add("Segundo");
        fila.add("Terceiro");
        
        // Imprimindo a fila
        System.out.println("Fila: " + fila);
        
        // Removendo o primeiro elemento (dequeue)
        String removido = fila.remove();
        System.out.println("Elemento removido: " + removido);
        System.out.println("Fila após remoção: " + fila);
        
        // Espiando o próximo elemento (sem remover)
        String proximo = fila.peek();
        System.out.println("Próximo elemento: " + proximo);
        System.out.println("Fila permanece: " + fila);
    }
}
