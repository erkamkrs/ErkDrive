<script lang="ts">
	import { get } from "svelte/store";
	import { token } from "$lib/stores/auth";

	export let onUploadComplete: () => Promise<void>;
	export let folderId: string = "root";

	let file: File | null = null;
	let isUploading = false;
	let uploadStatus = { message: "", isError: false };
	let isDragOver = false;

	function handleDragOver(e: DragEvent) {
		e.preventDefault();
		isDragOver = true;
	}

	function handleDragLeave() {
		isDragOver = false;
	}

	function handleDrop(e: DragEvent) {
		e.preventDefault();
		isDragOver = false;
		if (e.dataTransfer?.files) {
			file = e.dataTransfer.files[0];
		}
	}

	async function uploadFile() {
		if (!file) return;

		isUploading = true;
		uploadStatus = { message: "", isError: false };

		try {
			const formData = new FormData();
			formData.append("file", file);

			const jwt = get(token);
			const response = await fetch(
				`http://localhost:8000/upload?folder=${folderId}`,
				{
					method: "POST",
					body: formData,
					headers: {
						Authorization: `Bearer ${jwt}`
					}
				}
			);

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.detail || "Upload failed");
			}

			uploadStatus = {
				message: "File uploaded successfully!",
				isError: false
			};
			await onUploadComplete();
			file = null;
		} catch (error) {
			uploadStatus = {
				message: `Error: ${error instanceof Error ? error.message : String(error)}`,
				isError: true
			};
		} finally {
			isUploading = false;
		}
	}
</script>

<div class="mb-6">
	<div
		role="region"
		aria-label="File upload area"
		class={`border-2 ${isDragOver ? "border-blue-500 bg-blue-50" : "border-dashed border-gray-300"} rounded-lg p-8 transition-colors duration-200`}
		on:dragover={handleDragOver}
		on:dragleave={handleDragLeave}
		on:drop={handleDrop}
	>
		<div class="flex flex-col items-center justify-center text-center space-y-3">
			<svg class={`mx-auto h-14 w-14 ${isDragOver ? "text-blue-500" : "text-gray-400"}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
			</svg>
			<div class="mt-2 flex text-sm text-gray-600">
				<label
					for="file-upload"
					class="relative cursor-pointer rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500"
				>
					<span>Upload a file</span>
					<input
						id="file-upload"
						name="file-upload"
						type="file"
						class="sr-only"
						on:change={(e) => {
							const target = e.target as HTMLInputElement | null;
							file = target?.files?.[0] ?? null;
						}}
					/>
				</label>
				<p class="pl-1">or drag and drop</p>
			</div>
			{#if file}
				<p class="mt-1 text-xs text-gray-500">
					Selected: <span class="font-medium">{file.name}</span>
					({#if file.size < 1024}
						{file.size} bytes
					{:else if file.size < 1048576}
						{(file.size / 1024).toFixed(1)} KB
					{:else}
						{(file.size / 1048576).toFixed(1)} MB
					{/if})
				</p>
			{:else}
				<p class="mt-1 text-xs text-gray-500">Supports PDF, images, documents up to 10MB</p>
			{/if}
		</div>
	</div>

	<div class="mt-4 flex justify-end">
		<button
			on:click={uploadFile}
			disabled={!file || isUploading}
			class={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white ${!file || isUploading ? "bg-blue-300 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
		>
			{#if isUploading}
				<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
				</svg>
				Uploading...
			{:else}
				Upload File
			{/if}
		</button>
	</div>

	{#if uploadStatus.message}
		<div class={`mt-4 rounded-md p-4 ${uploadStatus.isError ? "bg-red-50" : "bg-green-50"}`}>
			<div class="flex">
				<div class="flex-shrink-0">
					{#if uploadStatus.isError}
						<svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
							<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
						</svg>
					{:else}
						<svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
							<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
						</svg>
					{/if}
				</div>
				<div class="ml-3">
					<p class={`text-sm font-medium ${uploadStatus.isError ? "text-red-800" : "text-green-800"}`}>{uploadStatus.message}</p>
				</div>
			</div>
		</div>
	{/if}
</div>
