<script lang="ts">
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";

	let email = "";
	let password = "";
	let error = "";
	let success = "";

	let showToast = false;

	async function register() {
		error = "";
		const res = await fetch("http://localhost:8000/register", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ email, password }),
		});

		if (!res.ok) {
			const err = await res.json();
			error = err.detail || "Registration failed";
			return;
		}

		success = "Account created!";
		showToast = true;

		setTimeout(() => {
			showToast = false;
			goto("/login");
		}, 2000); // show toast for 2 seconds before redirect
	}
</script>

<style>
	.toast {
		position: fixed;
		top: 20px;
		right: 20px;
		background-color: #38a169;
		color: white;
		padding: 12px 16px;
		border-radius: 8px;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
		z-index: 50;
	}
</style>

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
			>Register to ErkDrive</a
		>
		<h2 class="text-xl my-2 text-gray-500">Register</h2>
	</div>
	<form on:submit|preventDefault={register} class="space-y-4 max-w-md mx-auto">
		<input type="email" bind:value={email} placeholder="Email" required class="w-full border p-2 rounded" />
		<input type="password" bind:value={password} placeholder="Password" required class="w-full border p-2 rounded" />
		<button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Register</button>

		{#if error}
			<p class="text-red-500">{error}</p>
		{/if}
		<p class="text-sm text-gray-600 mt-2">
			Already have an account? <a href="/login" class="text-blue-600 underline">Login</a>
		</p>
	</form>
</div>

{#if showToast}
	<div class="toast">
		{success}
	</div>
{/if}
