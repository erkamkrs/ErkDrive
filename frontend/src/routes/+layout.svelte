<script lang="ts">
	import "../app.css";
	import { token, user, logout } from "$lib/stores/auth";
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";

	let isLoggedIn = false;
	let email = "";

	// Listen to auth state
	$: isLoggedIn = !!$token;
	$: email = $user;

	function handleLogout() {
		logout();
		goto("/login");
	}

	onMount(() => {
		if (!$token) {
			goto("/login");
		}
	});
</script>

<svelte:head>
	<title>ErkDrive - Secure Cloud Storage</title>
	<meta name="description" content="Your secure file storage solution" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<link
		rel="icon"
		href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📁</text></svg>"
	/>
</svelte:head>

<div class="min-h-screen bg-gray-50 flex flex-col">
	<!-- Header -->
	<header class="bg-gradient-to-r from-blue-600 to-blue-800 shadow-lg">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between items-center py-4">
				<!-- Logo -->
				<div class="flex items-center space-x-3">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-8 w-8 text-white"
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
					<a href="/" class="text-2xl font-bold text-white"
						>ErkDrive</a
					>
				</div>

				<!-- Auth Controls -->
				<div class="text-sm text-white flex items-center gap-4">
					{#if isLoggedIn}
						<span class="hidden sm:inline">Hello, {$user}</span>
						<button
							class="bg-white text-blue-700 font-semibold px-3 py-1 rounded hover:bg-gray-100"
							on:click={handleLogout}
						>
							Log out
						</button>
					{:else}
						<a href="/login" class="hover:underline">Log in</a>
						<a href="/register" class="hover:underline">Register</a>
					{/if}
				</div>
			</div>
		</div>
	</header>

	<!-- Page Content -->
	<main class="flex-grow">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
			<slot />
		</div>
	</main>

	<!-- Footer -->
	<footer class="bg-white border-t border-gray-200">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
			<div class="flex flex-col md:flex-row justify-between items-center">
				<p class="text-sm text-gray-500">
					&copy; {new Date().getFullYear()} ErkDrive. All rights reserved.
				</p>
				<div class="mt-2 md:mt-0 flex space-x-6">
					<!-- <a href="#" class="text-sm text-gray-500 hover:text-gray-700">Terms</a>
					<a href="#" class="text-sm text-gray-500 hover:text-gray-700">Privacy</a>
					<a href="#" class="text-sm text-gray-500 hover:text-gray-700">Contact</a> -->
				</div>
			</div>
		</div>
	</footer>
</div>
