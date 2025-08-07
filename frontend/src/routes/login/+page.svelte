<script lang="ts">
	import { token, user } from "$lib/stores/auth";
	import { goto } from "$app/navigation";

	let email = "";
	let password = "";
	let error = "";

	async function login() {
    error = "";
    try {
        const res = await fetch("http://localhost:8000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (!res.ok) {
            const err = await res.json();
            error = err.detail || "Login failed";
            console.error("Login error:", err); // Add this line
            return;
        }

        const data = await res.json();
        token.set(data.access_token);
        user.set(email);
        goto("/");
    } catch (err) {
        console.error("Network error:", err); // Add this line
        error = "Network error - could not reach server";
    }
}
</script>

<div class="flex flex-col gap-12 items-center justify-center min-h-screen">
	<div class="flex flex-col items-center justify-center">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			class="h-20 w-20 text-blue-600 hover:text-blue-800"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
			/>
		</svg>
		<a href="/" class="text-2xl font-bold text-blue-600 hover:text-blue-800"
			>Welcome to ErkDrive</a
		>
		<h2 class="text-xl my-2 text-gray-500">Login to your account</h2>
	</div>
	{#if $user}
		<p class="text-green-500 mb-4">Logged in as {$user}</p>
	{/if}
	<form on:submit|preventDefault={login} class="space-y-4 max-w-md mx-auto">
		<input
			type="email"
			bind:value={email}
			placeholder="Email"
			required
			class="w-full border p-2 rounded"
		/>
		<input
			type="password"
			bind:value={password}
			placeholder="Password"
			required
			class="w-full border p-2 rounded"
		/>
		<button
			type="submit"
			class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
			>Login</button
		>

		{#if error}
			<p class="text-red-500">{error}</p>
		{/if}
		<p class="text-sm text-gray-600 mt-2">
			Don't have an account? <a
				href="/register"
				class="text-blue-600 underline">Register</a
			>
		</p>
	</form>
</div>
