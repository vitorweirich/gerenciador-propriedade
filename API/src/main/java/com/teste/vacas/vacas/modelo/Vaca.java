package com.teste.vacas.vacas.modelo;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
//@JsonPropertyOrder({"ensiminacao", "nome", "nCrias", "parto"})
public class Vaca {

	private static DateTimeFormatter formater = DateTimeFormatter.ofPattern("dd/MM/yyyy");

	@Id
	private String numero;
	private String nome;
	private LocalDate ensiminacao;
	private LocalDate secagem;
	private LocalDate parto;
	private LocalDate novaEnsiminacao;
	private Integer nCrias;
	private String cor;

	public Vaca() {
		super();
	}

	public Vaca(String numero, String nome, Integer nCrias) {
		super();
		this.numero = numero;
		this.nome = nome;
		this.nCrias = nCrias;
	}

	public Vaca(String numero, String nome, String ensiminacao, String secagem, String parto, String novaEnsiminacao,
			Integer nCrias, String cor) {
		super();
		this.numero = numero;
		this.nome = nome;
		this.ensiminacao = LocalDate.parse(ensiminacao, formater);
		this.secagem = LocalDate.parse(secagem, formater);
		this.parto = LocalDate.parse(parto, formater);
		this.novaEnsiminacao = LocalDate.parse(novaEnsiminacao, formater);
		this.nCrias = nCrias;
		this.cor = cor;
	}

	public String getNumero() {
		return numero;
	}

	public void setNumero(String numero) {
		this.numero = numero;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public LocalDate getEnsiminacao() {
		return ensiminacao;
	}

	public void setEnsiminacao(LocalDate ensiminacao) {
		this.ensiminacao = ensiminacao;
	}

	public LocalDate getSecagem() {
		return secagem;
	}

	public void setSecagem(LocalDate secagem) {
		this.secagem = secagem;
	}

	public LocalDate getParto() {
		return parto;
	}

	public void setParto(LocalDate parto) {
		this.parto = parto;
	}

	public LocalDate getNovaEnsiminacao() {
		return novaEnsiminacao;
	}

	public void setNovaEnsiminacao(LocalDate novaEnsiminacao) {
		this.novaEnsiminacao = novaEnsiminacao;
	}

	public Integer getnCrias() {
		return nCrias;
	}

	public void setnCrias(Integer nCrias) {
		this.nCrias = nCrias;
	}

	public String getCor() {
		return cor;
	}

	public void setCor(String cor) {
		this.cor = cor;
	}

}
