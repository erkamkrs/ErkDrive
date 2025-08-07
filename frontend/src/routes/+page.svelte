<script lang="ts">
  import FileBrowser from '$lib/components/FileBrowser.svelte';
  import { token } from '$lib/stores/auth';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  onMount(() => {
    if (!$token) {
      goto('/login');
    }
  });
</script>

{#if $token}
  <FileBrowser />
{:else}
  <p class="text-center mt-20 text-gray-500">Redirecting to login...</p>
{/if}
