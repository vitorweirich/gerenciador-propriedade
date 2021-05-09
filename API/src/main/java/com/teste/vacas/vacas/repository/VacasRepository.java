package com.teste.vacas.vacas.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.teste.vacas.vacas.modelo.Vaca;

@Repository
public interface VacasRepository extends JpaRepository<Vaca, String> {

	List<Vaca> findAllByOrderByNome();

	List<Vaca> findByNomeIgnoreCaseContainingOrNumeroContainingOrderByNome(String nome, String numero);

}
