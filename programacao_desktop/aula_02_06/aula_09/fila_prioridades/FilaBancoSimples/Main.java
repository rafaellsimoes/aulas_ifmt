import java.util.PriorityQueue;
import java.util.Queue;

class BancoSimples {
    public static void main(String[] args) {
        // Cria a fila de prioridade
        Queue<cliente> fila = new PriorityQueue<>(
            (c1, c2) -> {
                // Prioritários primeiro
                if(c1.prioritario && !c2.prioritario) return -1;
                if(!c1.prioritario && c2.prioritario) return 1;
                return 0; 
            }
        );
        
        fila.add(new cliente("João", false));
        fila.add(new cliente("Maria", true));
        fila.add(new cliente("Pedro", false));
        fila.add(new cliente("Ana", true));
        
   
        System.out.println("Clientes na fila: " + fila);
        
        // Atende um por um
        System.out.println("\nAtendendo:");
        while(!fila.isEmpty()) {
            cliente cliente = fila.poll();
            System.out.println("Atendendo: " + cliente);
        }
    }
}
