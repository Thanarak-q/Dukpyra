var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// --- Dukpyra Generated Routes ---

app.MapGet("/", () =>
{
    return Results.Ok(new { message = "HI from dukpyra" });
});

app.MapGet("/health", () =>
{
    return Results.Ok(new { status = "ok", version = "2.0" });
});

// --------------------------------

app.Run();