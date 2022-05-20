package com.example.webservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@EnableJpaAuditing
@SpringBootApplication
public class SpringWebserviceApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringWebserviceApplication.class, args);
    }

}
