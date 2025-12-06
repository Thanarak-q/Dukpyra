var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// --- Dukpyra Generated Routes ---

app.MapGet("/", () =>
{
    return Results.Ok(new { message = "HI from dukpyra i am 4 year old" });
});

app.MapGet("/health", () =>
{
    return Results.Ok(new { status = "ok", version = "2.0" });
});

app.MapGet("/test", () =>
{
    return Results.Ok(new { message = "test" });
});

app.MapGet("/test2", () =>
{
    return Results.Ok(new { message = "test" });
});

app.MapGet("/test3", () =>
{
    return Results.Ok(new { message = "test" });
});

// --------------------------------

app.Run();