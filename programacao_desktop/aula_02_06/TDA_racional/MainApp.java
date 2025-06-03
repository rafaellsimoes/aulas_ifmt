import java.util.InputMismatchException;
import java.util.Scanner;

public class App {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
    
        try {
            System.out.println("Digite a primeira fração (N / D):");
            double N1 = scanner.nextDouble();
            scanner.next(); 
            double D1 = scanner.nextDouble();

        
            System.out.println("Digite a segunda fração (N / D):");
            double N2 = scanner.nextDouble();
            scanner.next(); 
            double D2 = scanner.nextDouble();

     
            Fracao f1 = new Fracao(N1, D1);
            Fracao f2 = new Fracao(N2, D2);
            System.out.println("Primeira Fracao"+f1.toString());
            System.out.println("Segunda Fracao"+f2.toString());
            Fracao resultado = f1.soma(f2); 
            System.out.println("Soma: " + resultado.toString());

        } catch (InputMismatchException e) {
            System.out.println("Erro: Digite números válidos (ex: 1.5 / 2.0)");
        } catch (ArithmeticException e) {
            System.out.println("Erro: " + e.getMessage());
        } finally {
            scanner.close();
        }
    }
}
