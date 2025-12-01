<template>
    <PvMenubar
        :model="items"
        :style="{
            borderRadius: 0,
            border: 0,
        }"
    >
        <template #start>
            <BhmNavbarLogo />
        </template>

        <template #item="{ item, props }">
            <PvButton text class="menu-item" v-bind="props">
                <NuxtLink v-bind="props" :to="item.to">
                    <Icon
                        v-if="item.icon"
                        :name="item.icon"
                        :style="{ marginRight: '0.3rem' }"
                    />
                    <span>{{ item.label }}</span>
                </NuxtLink>
            </PvButton>
        </template>

        <template #itemicon="{ item }">
            <Icon :name="item.icon" />
        </template>
    </PvMenubar>
</template>

<script setup>
const items = ref([
    {
        label: "Test",
        icon: "material-symbols:house",
        to: "/test",
    },
]);
</script>

<style scoped>
.menu-item a {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}

a {
    text-decoration: none;
    color: var(--pv-text-primary);
}
</style>
