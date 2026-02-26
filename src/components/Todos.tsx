import React, { useEffect, useState, createContext, useContext } from "react";
import {
  Container,
  Stack,
  Text,
  Spinner,
  Input,
  Button,
  Flex,
} from "@chakra-ui/react";

interface Todo {
  id: string;
  item: string;
}

interface TodosContextType {
  todos: Todo[];
  fetchTodos: () => Promise<void>;
}

interface UpdateTodoProps {
  id: string;
  item: string;
  fetchTodos: () => Promise<void>;
}

interface DeleteTodoProps {
  id: string;
  fetchTodos: () => Promise<void>;
}

// --- Contexto ---
const TodosContext = createContext<TodosContextType>({
  todos: [],
  fetchTodos: async () => {},
});

// --- Adicionar Tarefa ---
function AddTodo() {
  const [item, setItem] = useState("");
  const { todos, fetchTodos } = useContext(TodosContext);

  const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    setItem(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!item.trim()) return;

    const newTodo = {
      id: String(todos.length + 1),
      item: item,
    };

    await fetch("http://localhost:8000/todo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newTodo),
    });

    setItem("");
    fetchTodos();
  };

  return (
    <form onSubmit={handleSubmit}>
      <Flex gap={3} mt={5}>
        <Input
          pr="4.5rem"
          type="text"
          placeholder="Adicionar tarefa..."
          aria-label="Add a todo item"
          value={item}
          onChange={handleInput}
        />
        <Button type="submit" colorScheme="blue">
          Adicionar
        </Button>
      </Flex>
    </form>
  );
}

// --- Atualizar Tarefa ---
const UpdateTodo = ({ id, item, fetchTodos }: UpdateTodoProps) => {
  const [todo, setTodo] = useState(item);
  const [isEditing, setIsEditing] = useState(false);

  const updateTodo = async () => {
    await fetch(`http://localhost:8000/todo/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: id, item: todo }),
    });
    setIsEditing(false);
    await fetchTodos();
  };

  return (
    <Flex gap={2} alignItems="center">
      {isEditing ? (
        <>
          <Input
            value={todo}
            onChange={(e) => setTodo(e.target.value)}
            size="sm"
          />
          <Button h="1.5rem" size="sm" colorScheme="green" onClick={updateTodo}>
            Salvar
          </Button>
        </>
      ) : (
        <>
          <Text fontWeight="bold">{item}</Text>
          <Button
            h="1.5rem" size="sm"
            colorScheme="yellow"
            onClick={() => setIsEditing(true)}
          >
            Editar
          </Button>
        </>
      )}
    </Flex>
  );
};

// --- Excluir Tarefa ---
const DeleteTodo = ({ id, fetchTodos }: DeleteTodoProps) => {
  const deleteTodo = async () => {
    await fetch(`http://localhost:8000/todo/${id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: id }),
    });
    await fetchTodos();
  }; 

  return (
    <Button h="1.5rem" size="sm" colorScheme="red" onClick={deleteTodo}>
      Excluir
    </Button>
  );
};

// --- Componente Principal ---
export default function Todos() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchTodos = async () => {
    try {
      const response = await fetch("http://localhost:8000/todo");
      const data = await response.json();
      console.log("Resposta da API:", data);
      setTodos(data.data || data);
    } catch (error) {
      console.error("Erro ao buscar todos:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <TodosContext.Provider value={{ todos, fetchTodos }}>
      <Container maxW="container.xl" pt="100px">
        <AddTodo />
        {loading ? (
          <Spinner />
        ) : todos.length === 0 ? (
          <Text mt={5}>Nenhuma tarefa encontrada.</Text>
        ) : (
          <Stack gap={3} mt={5}>
            {todos.map((todo) => (
              <Flex key={todo.id} alignItems="center" justifyContent="space-between">
                <UpdateTodo id={todo.id} item={todo.item} fetchTodos={fetchTodos} />
                <DeleteTodo id={todo.id} fetchTodos={fetchTodos} />
              </Flex>
            ))}
          </Stack>
        )}
      </Container>
    </TodosContext.Provider>
  );
}
