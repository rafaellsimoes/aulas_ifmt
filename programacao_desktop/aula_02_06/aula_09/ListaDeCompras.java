import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int numListas = scanner.nextInt();
        scanner.nextLine();
        
        for (int i = 0; i < numListas; i++) {
       
            int numItens = scanner.nextInt();
            scanner.nextLine(); 
            
            List<String> itens = new ArrayList<>();
            
          
            for (int j = 0; j < numItens; j++) {
                String item = scanner.nextLine().trim();
  
                if (!item.isEmpty() && !itens.contains(item)) {
                    itens.add(item);
                }
            }
            
            Collections.sort(itens);
            
            for (int k = 0; k < itens.size(); k++) {
                System.out.print(itens.get(k));
                if (k < itens.size() - 1) {
                    System.out.print(" ");
                }
            }
            System.out.println();
        }
        
        scanner.close();
    }
}
