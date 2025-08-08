<script lang="ts">
    import { onMount } from "svelte";
    import FileUpload from "./FileUpload.svelte";
    import Modal from "./Modal.svelte";

    type FileItem = {
        id: string;
        filename: string;
        size?: number;
        upload_date: string;
        content_type?: string;
        is_folder?: boolean;
    };

    type Folder = {
        id: string;
        name: string;
    };

    let files: FileItem[] = [];
    let folderPath: Folder[] = [{ id: "root", name: "root" }];
    let isLoading = true;
    let error = "";
    let searchQuery = "";
    let sortField: "filename" | "upload_date" | "size" = "filename";
    let sortOrder: "asc" | "desc" = "asc";
    let previewFile: FileItem | null = null;
    let showPreview = false;
    let activeSort = {
        field: "filename",
        order: "asc"
    };
    let showSortDropdown = false;

    function currentFolderId(): string {
        return folderPath[folderPath.length - 1].id;
    }

    onMount(fetchFiles);

    async function fetchFiles() {
        try {
            isLoading = true;
            let url = `http://localhost:8000/files?folder=${currentFolderId()}&sort_by=${sortField}&sort_order=${sortOrder}`;
            
            if (searchQuery) {
                url = `http://localhost:8000/search?query=${encodeURIComponent(searchQuery)}`;
            }

            const response = await fetch(url);
            files = await response.json();
            error = "";
        } catch (err) {
            error = "Failed to load files";
            console.error(err);
        } finally {
            isLoading = false;
        }
    }

    async function createFolder() {
        const name = prompt("Folder name:");
        if (!name) return;

        await fetch(
            `http://localhost:8000/folders?name=${encodeURIComponent(name)}`,
            {
                method: "POST",
            },
        );

        await fetchFiles();
    }

    function openFolder(file: FileItem) {
        folderPath = [...folderPath, { id: file.id, name: file.filename }];
        fetchFiles();
    }

    function goToFolder(index: number) {
        folderPath = folderPath.slice(0, index + 1);
        fetchFiles();
    }

    async function handleDelete(id: string) {
        if (!confirm("Are you sure you want to delete this file?")) return;

        try {
            await fetch(`http://localhost:8000/files/${id}`, {
                method: "DELETE",
            });
            await fetchFiles();
        } catch (err) {
            console.error(err);
        }
    }

    function handlePreview(file: FileItem, event: MouseEvent) {
        event.stopPropagation();
        if (file.is_folder) return;
        
        if (file.content_type?.startsWith("image/") || file.content_type === "application/pdf") {
            previewFile = file;
            showPreview = true;
        }
    }

    function handleSort(field: "filename" | "upload_date" | "size") {
        if (sortField === field) {
            sortOrder = sortOrder === "asc" ? "desc" : "asc";
        } else {
            sortField = field;
            sortOrder = "asc";
        }
        fetchFiles();
    }

    function handleSearch() {
        fetchFiles();
    }
</script>

<div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
    <!-- Search Bar -->
    <div class="mb-6">
        <div class="relative rounded-md shadow-sm">
            <input
                type="text"
                bind:value={searchQuery}
                on:keyup={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Search files..."
                class="block w-full pr-12 sm:text-sm border-gray-300 rounded-md p-2 border"
            />
            <div class="absolute inset-y-0 right-0 flex items-center">
                <button
                    on:click={handleSearch}
                    class="px-4 h-full bg-blue-600 text-white rounded-r-md hover:bg-blue-700 focus:outline-none"
                >
                    Search
                </button>
            </div>
        </div>
    </div>

    <nav class="mb-2">
        <ol class="flex items-center space-x-2 text-base">
            {#each folderPath as folder, index}
                <li>
                    <div class="flex items-center">
                        {#if index > 0}
                            <svg
                                class="h-5 w-5 text-gray-400"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                            >
                                <path
                                    fill-rule="evenodd"
                                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                                    clip-rule="evenodd"
                                />
                            </svg>
                        {/if}
                        <button
                            on:click={() => goToFolder(index)}
                            class={`font-medium text-2xl ${index === folderPath.length - 1 ? "text-gray-500 hover:gray-blue-600" : "text-gray-300 hover:text-gray-400"}`}
                        >
                            {folder.name === "root" ? "Home" : folder.name}
                        </button>
                    </div>
                </li>
            {/each}
        </ol>
    </nav>

    <div class="flex justify-center mb-6">
        <div class="w-full max-w-2xl">
            <FileUpload
                onUploadComplete={fetchFiles}
                folderId={currentFolderId()}
            />
        </div>
    </div>

    <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6 text-blue-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
                />
            </svg>
            My Files
        </h2>
        
        <div class="flex items-center space-x-4">
            <button
                on:click={createFolder}
                class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="-ml-0.5 mr-1.5 h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                    />
                </svg>
                New Folder
            </button>
            
            <div class="relative">
                <button
                    on:click={() => showSortDropdown = !showSortDropdown}
                    class="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none"
                >
                    Sort: {sortField} ({sortOrder})
                </button>
                {#if showSortDropdown}
                    <div class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                        <div class="py-1">
                            <button
                                on:click={() => {
                                    handleSort("filename");
                                    showSortDropdown = false;
                                }}
                                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                            >
                                Name {sortField === "filename" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
                            </button>
                            <button
                                on:click={() => {
                                    handleSort("upload_date");
                                    showSortDropdown = false;
                                }}
                                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                            >
                                Date {sortField === "upload_date" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
                            </button>
                            <button
                                on:click={() => {
                                    handleSort("size");
                                    showSortDropdown = false;
                                }}
                                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                            >
                                Size {sortField === "size" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
                            </button>
                        </div>
                    </div>
                {/if}
            </div>
        </div>
    </div>

    {#if isLoading}
        <div class="flex justify-center items-center py-12">
            <div
                class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"
            ></div>
        </div>
    {:else if error}
        <div class="rounded-md bg-red-50 p-4 mb-4">
            <div class="flex">
                <div class="flex-shrink-0">
                    <svg
                        class="h-5 w-5 text-red-400"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                    >
                        <path
                            fill-rule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </div>
                <div class="ml-3">
                    <h3 class="text-sm font-medium text-red-800">{error}</h3>
                </div>
            </div>
        </div>
    {:else if files.length === 0}
        <div class="text-center py-12">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                class="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 13h6m-6 4h6m2 5H7a2 2 0 01-2-2V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z"
                />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No files</h3>
            <p class="mt-1 text-sm text-gray-500">
                Upload your first file or create a folder to get started.
            </p>
        </div>
    {:else}
        <div
            class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg"
        >
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th
                            scope="col"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                            on:click={() => handleSort("filename")}
                        >
                            <div class="flex items-center">
                                Name
                                {#if activeSort.field === 'filename'}
                                    <span class="ml-1">
                                        {activeSort.order === 'asc' ? '↑' : '↓'}
                                    </span>
                                {/if}
                            </div>
                        </th>
                        <th
                            scope="col"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                            on:click={() => handleSort("size")}
                        >
                            <div class="flex items-center">
                                Size
                                {#if activeSort.field === 'size'}
                                    <span class="ml-1">
                                        {activeSort.order === 'asc' ? '↑' : '↓'}
                                    </span>
                                {/if}
                            </div>
                        </th>
                        <th
                            scope="col"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                            on:click={() => handleSort("upload_date")}
                        >
                            <div class="flex items-center">
                                Modified
                                {#if activeSort.field === 'upload_date'}
                                    <span class="ml-1">
                                        {activeSort.order === 'asc' ? '↑' : '↓'}
                                    </span>
                                {/if}
                            </div>
                        </th>
                        <th
                            scope="col"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                            Actions
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    {#each files as file (file.id)}
                        <tr class="hover:bg-gray-50">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    {#if file.is_folder}
                                        <div
                                            class="flex-shrink-0 h-10 w-10 flex items-center justify-center text-blue-500"
                                        >
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                class="h-6 w-6"
                                                fill="none"
                                                viewBox="0 0 24 24"
                                                stroke="currentColor"
                                            >
                                                <path
                                                    stroke-linecap="round"
                                                    stroke-linejoin="round"
                                                    stroke-width="2"
                                                    d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
                                                />
                                            </svg>
                                        </div>
                                        <div class="ml-4">
                                            <button
                                                on:click={() => openFolder(file)}
                                                class="text-sm font-medium text-blue-600 hover:text-blue-500 hover:underline focus:outline-none"
                                            >
                                                {file.filename}
                                            </button>
                                        </div>
                                    {:else}
                                        <div
                                            class="flex-shrink-0 h-10 w-10 flex items-center justify-center text-gray-400"
                                        >
                                            {#if file.content_type?.startsWith("image/")}
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    class="h-6 w-6"
                                                    fill="none"
                                                    viewBox="0 0 24 24"
                                                    stroke="currentColor"
                                                >
                                                    <path
                                                        stroke-linecap="round"
                                                        stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                                                    />
                                                </svg>
                                            {:else if file.content_type === "application/pdf"}
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    class="h-6 w-6"
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
                                            {:else}
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    class="h-6 w-6"
                                                    fill="none"
                                                    viewBox="0 0 24 24"
                                                    stroke="currentColor"
                                                >
                                                    <path
                                                        stroke-linecap="round"
                                                        stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                                                    />
                                                </svg>
                                            {/if}
                                        </div>
                                        <div class="ml-4">
                                            <button
                                                on:click={(e) => handlePreview(file, e)}
                                                class="text-sm font-medium text-gray-900 hover:text-blue-600 truncate max-w-xs text-left"
                                                title={file.filename}
                                            >
                                                {file.filename}
                                            </button>
                                        </div>
                                    {/if}
                                </div>
                            </td>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                            >
                                {file.size
                                    ? (file.size / 1024).toFixed(2) + " KB"
                                    : "-"}
                            </td>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                            >
                                {new Date(
                                    file.upload_date,
                                ).toLocaleDateString()}
                                <span class="text-gray-400 ml-1">
                                    {new Date(
                                        file.upload_date,
                                    ).toLocaleTimeString([], {
                                        hour: "2-digit",
                                        minute: "2-digit",
                                    })}
                                </span>
                            </td>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm font-medium"
                            >
                                <div class="flex space-x-3">
                                    <a
                                        href={`http://localhost:8000/download/${file.id}`}
                                        class="text-blue-600 hover:text-blue-900 flex items-center"
                                        title="Download"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            class="h-5 w-5"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke="currentColor"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                                            />
                                        </svg>
                                    </a>
                                    <button
                                        on:click={() => handleDelete(file.id)}
                                        class="text-red-600 hover:text-red-900 flex items-center"
                                        title="Delete"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            class="h-5 w-5"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke="currentColor"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                                            />
                                        </svg>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
</div>

{#if showPreview && previewFile}
    <Modal onClose={() => showPreview = false}>
        <div class="p-4 max-w-6xl max-h-screen">
            <h3 class="text-lg font-medium mb-4">{previewFile.filename}</h3>
            
            {#if previewFile.content_type?.startsWith("image/")}
                <img
                    src={`http://localhost:8000/preview/${previewFile.id}`}
                    alt={previewFile.filename}
                    class="max-w-full max-h-[120vh] object-contain"
                />
            {:else if previewFile.content_type === "application/pdf"}
                <iframe
                    src={`http://localhost:8000/preview/${previewFile.id}`}
                    class="w-full h-120vh] border"
                    title={previewFile.filename}
                ></iframe>
            {/if}
            
            <div class="mt-4 flex justify-end">
                <button
                    on:click={() => showPreview = false}
                    class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded"
                >
                    Close
                </button>
            </div>
        </div>
    </Modal>
{/if}