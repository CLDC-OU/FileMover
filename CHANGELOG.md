# Changelog

## 1.4.0 (2026-03-13)

```diff
    | Fixed keep source behavior being inverted for all but "always" and "never" modes
    | Fixed interactive config builder always setting config values as lowercase even when it doesn't make sense
    | Fixed interactive config builder saving name and description fields as "name" and "description" instead of "mover_name" and "mover_description"
+   | Added interactive config builder flow for an existing file at the specified path when saving config to file with an option to overwrite

    | [BREAKING] Completely reworked the file matching configuration system
-   | Removed config options: "file_type", "file_types", "file_type_regex", "file_type_exclude_regex", "file_name", "file_names", "file_name_regex", "file_name_exclude_regex", "file_name_contains", "file_name_starts_with", "file_name_ends_with"
+   | Added config option "match_files"
+   | Added separate File Matching module to process file matching rules
-   | Removed file matching rule validation in interactive config builder
+   | Added case sensitivity option to file matching
```

## 1.3.0 (2026-02-24)

```diff
-   | Removed "keep_source" configuration option
+   | Added "keep_source_behavior" configuration option
+   | Added "destination_collision_behavior"
+   | Added "collision_avoidance_behavior" configuration option

+   | Added interactive file mover configuration helper
+   | Added robust file collision handling

+   | Added consistent file timestamp initialization
```

## 1.2.7 (2025-08-01)

```diff
-   | Removed nullable directories config
+   | Improved logging messages for clarity
```

## 1.2.6 (2025-08-01)

```diff
+   | Added utility functions to mover
```

## 1.2.5 (2026-08-01)

```diff
+   | Added properties to Mover (structural change only, no difference in functionality)
```

## 1.2.4 (2025-06-27)

```diff
    | Fixed critical bug that processed unmatched files
```

## 1.2.3 (2025-06-27)

```diff
    | Updated package name in documentation
+   | Added recursive file moving
```

## 1.2.2 (2025-06-20)

```diff
-   | Removed duplicate package entry
```

## 1.2.1 (2025-06-20)

```diff
+   | Added package finding configuration and future annotations
```

## 1.2.0 (2025-06-20)

```diff
    | Convert to package structure
+   | Added setuptools and fixed package locator
```

## 1.1.0 (2025-06-20)

```diff
+   | Added example configuration files
    | Renamed modules for functional clarity
```

## 1.0.2 (2025-06-20)

```diff
    | Fixed minor style error
```

## 1.0.1 (2025-06-19)

```diff
    | Change input type of Mover initialization to kwargs to simplify new config loading and so that MoverConfig is only required internally
```

## 1.0.0 (2025-06-19)

### Features

```diff
    | Initial release of the project with basic file moving functionality!
    | It do be movin those files (I haven't actually tested it yet... but I'm pretending that I trust it to work on the first try)
+   | Added support for moving files
+   | Added regex support for file matching on separate name and extension
+   | Added support for renaming the file while moving
+   | Added support for moving files to multiple directories
+   | Added support for copying files without moving them
+   | Added support for timestamping files in customizable formats and at customizable positions
+   | 
```
