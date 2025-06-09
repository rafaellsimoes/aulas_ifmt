import java.util.Scanner; 
import java.util.TreeSet;  
import java.util.Set;     

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        int numListas = scanner.nextInt();
        scanner.nextLine(); 
        
        for (int i = 0; i < numListas; i++) {

            int numItens = scanner.nextInt();
            scanner.nextLine(); 
            
            Set<String> itensUnicos = new TreeSet<>();

            for (int j = 0; j < numItens; j++) {
                String item = scanner.nextLine().trim();
                if (!item.isEmpty()) {
                    itensUnicos.add(item);
                }
            }
            System.out.println(String.join(" ", itensUnicos));
        }
        
        scanner.close();
    }
}
