class Fracao {
    public static double quociente(double numerador, double denominador) throws ArithmeticException {
        if (denominador == 0) {
            throw new ArithmeticException("Divisão por zero!"); 
            
        }
        return numerador / denominador;
    }
}
