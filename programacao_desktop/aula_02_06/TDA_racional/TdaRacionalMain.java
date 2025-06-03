public class Fracao {
    private double numerador;
    private double denominador;
    // Construtor
    public Fracao(double numerador, double denominador){
        if(denominador == 0){
            throw  new ArithmeticException("Denominador nulo");
        }
        this.numerador  = numerador;
        this.denominador = denominador;
    }
    // Getters 
    public double getNumerador(){
        return this.numerador;
    }
    public double getDenominador(){
        return this.denominador;
    }
    public Fracao soma(Fracao Fracao_soma){
        double Nnumerador = this.numerador*Fracao_soma.denominador + this.denominador*Fracao_soma.numerador;
        double NDenominador = this.denominador*Fracao_soma.denominador;
        return new Fracao(Nnumerador,NDenominador);
    }
    public Fracao subtracao(Fracao Fracao_dif) {
        double Nnumerador = this.numerador*Fracao_dif.denominador - this.denominador*Fracao_dif.numerador;
        double NDenominador = this.denominador*Fracao_dif.denominador;
        return new Fracao(Nnumerador,NDenominador);
    }

    public Fracao multiplicacao(Fracao Fracao_mul){
        double Nnumerador = this.numerador*Fracao_mul.numerador;
        double NDenominador = this.denominador*Fracao_mul.denominador;
        return  new Fracao(Nnumerador,NDenominador);
    }

    public Fracao divisao(Fracao Fracao_div){
        double Nnumerador = this.numerador*Fracao_div.denominador;
        double NDenominador = this.denominador*Fracao_div.numerador;
        return  new Fracao(Nnumerador,NDenominador);
    }

    @Override
    public String toString(){
        return  numerador + "/" + denominador;
    }

}
