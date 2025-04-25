document.addEventListener("DOMContentLoaded", () => {
    const submitButton = document.getElementById("submit");

    if (submitButton) {
        submitButton.addEventListener("click", async () => {
            const login = document.querySelector("input[type='login']").value;
            const password = document.querySelector("input[type='password']").value;

            if (!login || !password) {
                alert("Пожалуйста, заполните все поля!");
                return;
            }

            try {
                const response = await fetch("/users/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ login, password }),
                });

                if (response.ok) {
                    window.location.href = "/dashboard"; // Перенаправление на другую страницу
                } else {
                    alert("Ошибка входа. Проверьте логин и пароль.");
                }
            } catch (error) {
                console.error("Ошибка:", error);
                alert("Произошла ошибка. Попробуйте позже.");
            }
        });
    } else {
        console.error("Кнопка с id='submit' не найдена.");
    }
});