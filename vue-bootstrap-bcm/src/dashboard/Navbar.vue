<template>
    <!-- Navbar -->
    <nav
        class="main-header navbar navbar-expand navbar-dark"
        style="z-index: 98"
    >
        <!-- Left navbar links -->
        <ul class="navbar-nav">
            <li class="nav-item">
                <a
                    class="nav-link"
                    data-widget="pushmenu"
                    href="#"
                    role="button"
                >
                    <i class="fas fa-bars"></i>
                </a>
            </li>
        </ul>

        <!-- Right navbar links -->
        <ul class="navbar-nav ml-auto">
            <button class="btn btn-success">Logout</button>
            <a class="text-white mt-2"> correo@gmail.com </a>
            <!--a class="text-white mt-2">{{ logged_user?.email }} </a-->

            <!-- Notifications Dropdown Menu -->
            <li class="nav-item dropdown">
                <a class="nav-link" data-toggle="dropdown" href="#">
                    <i class="far fa-bell" style="font-size: 27px"></i>
                    <span
                        class="badge badge-warning navbar-badge"
                        style="font-size: 11px"
                        >15</span
                    >
                </a>
                <div class="dropdown-menu dropdown-menu-lg dropdown-menu-right">
                    <span class="dropdown-item dropdown-header"
                        >15 Notifications</span
                    >
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-envelope mr-2"></i> 4 new messages
                        <span class="float-right text-muted text-sm"
                            >3 mins</span
                        >
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-users mr-2"></i> 8 friend requests
                        <span class="float-right text-muted text-sm"
                            >12 hours</span
                        >
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-file mr-2"></i> 3 new reports
                        <span class="float-right text-muted text-sm"
                            >2 days</span
                        >
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item dropdown-footer"
                        >See All Notifications</a
                    >
                </div>
            </li>
            <li class="nav-item dropdown">
                <a class="nav-link" data-toggle="dropdown" href="#">
                    <i class="fas fa-user-circle user-size"></i>
                </a>
            </li>
        </ul>
    </nav>
    <!-- /.navbar -->
</template>

<script>
export default {};
</script>

<style>
</style>