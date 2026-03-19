buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath("com.android.tools.build:gradle:8.9.1")
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:2.1.0")
    }
}

allprojects {
    // تم حذف repositories من هنا لأنها معرفة في settings.gradle.kts
}

tasks.register<Delete>("clean") {
    delete(rootProject.layout.buildDirectory)
}
