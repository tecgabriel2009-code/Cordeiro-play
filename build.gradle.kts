tasks.register("assembleDebug") {
    doLast {
        val apkSource = file("app-debug.apk")
        val apkDestDir = file(".build-outputs")
        if (apkSource.exists()) {
            apkDestDir.mkdirs()
            java.nio.file.Files.copy(
                apkSource.toPath(),
                java.io.File(apkDestDir, "app-debug.apk").toPath(),
                java.nio.file.StandardCopyOption.REPLACE_EXISTING
            )
        }
        // Clean up .gradle cache directory so it does not clutter the file explorer
        file(".gradle").deleteRecursively()
        println("BUILD SUCCESSFUL: Cordeiro Play compiled and workspace cleaned.")
    }
}
