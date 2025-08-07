import { writable } from "svelte/store";
import { browser } from "$app/environment";

export const token = writable(browser ? localStorage.getItem("token") || "" : "");
export const user = writable(browser ? localStorage.getItem("user") || "" : "");

if (browser) {
	token.subscribe((val) => {
		localStorage.setItem("token", val);
	});
	user.subscribe((val) => {
		localStorage.setItem("user", val);
	});
}

export function logout() {
	token.set("");
	user.set("");
	if (browser) {
		localStorage.removeItem("token");
		localStorage.removeItem("user");
	}
}
