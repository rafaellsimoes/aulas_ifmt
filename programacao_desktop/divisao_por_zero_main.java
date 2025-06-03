import java.util.InputMismatchException;
import java.util.Scanner;

public class App {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean prossegueLoop = true;

        do {
            try {
                System.out.print("numerador: ");
                double numerador = scanner.nextDouble();
                System.out.print("Denominador: ");
                double denominador = scanner.nextDouble();

                double resultado = Fracao.quociente(numerador, denominador); // Corrigido para chamar Fracao.quociente()
                System.out.printf("\nResultado: %f / %f = %f\n", numerador, denominador, resultado);
                prossegueLoop = false;
            } catch (InputMismatchException inputMismatchException) {
                System.err.printf("\nException: %s\n", inputMismatchException);
                scanner.nextLine();
                System.err.println("Insira dois numeros");
            } catch (ArithmeticException arithmeticException) {
                System.err.printf("\nException: %s\n", arithmeticException);
                scanner.nextLine();
                System.err.println("Divisao por zero");
            }
        } while (prossegueLoop);
    }
}
