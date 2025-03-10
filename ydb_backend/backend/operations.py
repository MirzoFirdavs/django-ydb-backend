from django.db.backends.base.operations import BaseDatabaseOperations


class DatabaseOperations(BaseDatabaseOperations):
    cast_data_types = {
        "AutoField": "CAST(%(expression)s AS Uint64)",
        "BigAutoField": "CAST(%(expression)s AS Uint64)",
        "BinaryField": "CAST(%(expression)s AS String)",
        "BooleanField": "CAST(%(expression)s AS Bool)",
        "CharField": "CAST(%(expression)s AS Utf8)",
        "DateField": "CAST(%(expression)s AS Date)",
        "DateTimeField": "CAST(%(expression)s AS Datetime)",
        "DecimalField": "CAST(%(expression)s AS "
                        "Decimal(%(max_digits)s, %(decimal_places)s))",
        "DurationField": "CAST(%(expression)s AS Interval)",
        "FloatField": "CAST(%(expression)s AS Double)",
        "IntegerField": "CAST(%(expression)s AS Int32)",
        "BigIntegerField": "CAST(%(expression)s AS Int64)",
        "IPAddressField": "CAST(%(expression)s AS Utf8)",
        "GenericIPAddressField": "CAST(%(expression)s AS Utf8)",
        "JSONField": "CAST(%(expression)s AS Json)",
        "PositiveIntegerField": "CAST(%(expression)s AS Uint32)",
        "PositiveSmallIntegerField": "CAST(%(expression)s AS Uint16)",
        "SmallIntegerField": "CAST(%(expression)s AS Int16)",
        "TextField": "CAST(%(expression)s AS Utf8)",
        "TimeField": "CAST(%(expression)s AS Datetime)",
        "UUIDField": "CAST(%(expression)s AS Utf8)",
    }

    integer_field_ranges = {
        **BaseDatabaseOperations.integer_field_ranges,
    }

    set_operators = {
        "union": "UNION",
        "intersection": "INTERSECT",
        "difference": "EXCEPT",
    }

    cast_char_field_without_max_length = "String"

    def format_for_duration_arithmetic(self, sql):
        return f"DateTime::ToMicroseconds({sql})"

    def date_extract_sql(self, lookup_type, sql, params):
        if lookup_type == "year":
            return f"DateTime::GetYear({sql})", params
        if lookup_type == "month":
            return f"DateTime::GetMonth({sql})", params
        if lookup_type == "day":
            return f"DateTime::GetDay({sql})", params
        msg = f"Unsupported lookup type: {lookup_type}"
        raise ValueError(msg)

    def date_trunc_sql(self, lookup_type, sql, params, tzname=None):
        if tzname:
            sql = f"DateTime::MakeTzTimestamp({sql}, {tzname})"

        if lookup_type == "year":
            return f"DateTime::MakeDate(DateTime::GetYear({sql}), 1, 1)", params
        if lookup_type == "month":
            return (
                f"DateTime::MakeDate(DateTime::GetYear({sql}), "
                f"DateTime::GetMonth({sql}), 1)",
                params,
            )
        if lookup_type == "day":
            return (
                f"DateTime::MakeDate(DateTime::GetYear({sql}), "
                f"DateTime::GetMonth({sql}), "
                f"DateTime::GetDay({sql}))",
                params,
            )
        msg = f"Unsupported lookup type: {lookup_type}"
        raise ValueError(msg)

    def datetime_cast_date_sql(self, sql, params, tzname):
        sql = f"DateTime::MakeTzTimestamp({sql}, '{tzname}')"
        return f"DateTime::GetDate({sql})", params

    def datetime_cast_time_sql(self, sql, params, tzname):
        sql = f"DateTime::MakeTzTimestamp({sql}, '{tzname}')"
        return f"DateTime::GetTime({sql})", params

    def datetime_extract_sql(self, lookup_type, sql, params, tzname):
        sql = f"DateTime::MakeTzTimestamp({sql}, '{tzname}')"

        if lookup_type == "year":
            return f"DateTime::GetYear({sql})", params
        if lookup_type == "month":
            return f"DateTime::GetMonth({sql})", params
        if lookup_type == "day":
            return f"DateTime::GetDay({sql})", params
        if lookup_type == "hour":
            return f"DateTime::GetHour({sql})", params
        if lookup_type == "minute":
            return f"DateTime::GetMinute({sql})", params
        if lookup_type == "second":
            return f"DateTime::GetSecond({sql})", params
        msg = f"Unsupported lookup type: {lookup_type}"
        raise ValueError(msg)

    def datetime_trunc_sql(self, lookup_type, sql, params, tzname):
        sql = f"DateTime::MakeTzTimestamp({sql}, '{tzname}')"

        if lookup_type == "year":
            return (
                f"DateTime::MakeDatetime(DateTime::GetYear({sql}), 1, 1, 0, 0, 0)",
                params,
            )
        if lookup_type == "month":
            return (
                f"DateTime::MakeDatetime(DateTime::GetYear({sql}), "
                f"DateTime::GetMonth({sql}), 1, 0, 0, 0)",
                params,
            )
        if lookup_type == "day":
            return (
                f"DateTime::MakeDatetime(DateTime::GetYear({sql}), "
                f"DateTime::GetMonth({sql}), DateTime::GetDay({sql}), 0, 0, 0)",
                params,
            )
        if lookup_type == "hour":
            return (
                f"DateTime::MakeDatetime(DateTime::GetYear({sql}),"
                f"DateTime::GetMonth({sql}), "
                f"DateTime::GetDay({sql}), "
                f"DateTime::GetHour({sql}), 0, 0)",
                params,
            )
        if lookup_type == "minute":
            return (
                f"DateTime::MakeDatetime(DateTime::GetYear({sql}),"
                f"DateTime::GetMonth({sql}), "
                f"DateTime::GetDay({sql}), "
                f"DateTime::GetHour({sql}), "
                f"DateTime::GetMinute({sql}), 0)",
                params,
            )
        if lookup_type == "second":
            return (
                f"DateTime::MakeDatetime(DateTime::GetYear({sql}),"
                f"DateTime::GetMonth({sql}), "
                f"DateTime::GetDay({sql}), "
                f"DateTime::GetHour({sql}), "
                f"DateTime::GetMinute({sql}), "
                f"DateTime::GetSecond({sql}))",
                params,
            )
        msg = f"Unsupported lookup type: {lookup_type}"
        raise ValueError(msg)

    def time_trunc_sql(self, lookup_type, sql, params, tzname=None):
        if tzname:
            sql = f"DateTime::MakeTzTimestamp({sql}, '{tzname}')"

        if lookup_type == "hour":
            return f"DateTime::MakeTime(DateTime::GetHour({sql}), 0, 0)", params
        if lookup_type == "minute":
            return (
                f"DateTime::MakeTime(DateTime::GetHour({sql}) ,"
                f"DateTime::GetMinute({sql}), 0)",
                params,
            )
        if lookup_type == "second":
            return (
                f"DateTime::MakeTime(DateTime::GetHour({sql}), "
                f"DateTime::GetMinute({sql}), DateTime::GetSecond({sql}))",
                params,
            )
        msg = f"Unsupported lookup type: {lookup_type}"
        raise ValueError(msg)

    def no_limit_value(self):
        return None

    def quote_name(self, name):
        if name.startswith("`") and name.endswith("`"):
            return name  # Quoting once is enough.
        return f'"{name}"'

    def regex_lookup(self, lookup_type):
        if lookup_type == "regex":
            return "%s REGEXP %s"
        if lookup_type == "iregex":
            return "LOWER(%s) REGEXP LOWER(%s)"
        msg = f"Lookup '{lookup_type}' is not supported."
        raise NotImplementedError(msg)

    def sql_flush(self, style, tables, *, reset_sequences=False, allow_cascade=False):
        if not tables:
            return []

        sql_list = []
        for table in tables:
            sql_list.append(f"DELETE FROM {self.quote_name(table)}")

        if reset_sequences:
            for table in tables:
                sql_list.append(
                    f"ALTER SEQUENCE {self.quote_name(table + '_seq')} RESTART WITH 1"
                )

        return sql_list
