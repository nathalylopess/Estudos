create table usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
);

create table exercicios (
    matricula TEXT NOT NULL,
    exercicio TEXT NOT NULL,
    descricao TEXT NOT NULL
);