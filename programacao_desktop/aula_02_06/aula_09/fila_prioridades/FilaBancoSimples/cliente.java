class cliente {
    String nome;
    boolean prioritario; // true = prioritário, false = normal
    
    public cliente(String nome, boolean prioritario) {
        this.nome = nome;
        this.prioritario = prioritario;
    }
    
    @Override
    public String toString() {
        return nome + (prioritario ? " (P)" : "");
    }
}
