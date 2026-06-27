from django.views.generic import FormView
from .models import guest
from .forms import Quiz, Quiz_dop

class QuizView(FormView):
    form_class = Quiz
    template_name = 'main.html'
    formset_prefix = 'guests'  # <-- ЕДИНЫЙ prefix для formset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'formset' not in context:
            if self.request.method == 'POST':
                context['formset'] = Quiz_dop(self.request.POST, prefix=self.formset_prefix)
            else:
                context['formset'] = Quiz_dop(prefix=self.formset_prefix)

        context.setdefault('success', False)
        context.setdefault('guest_name', None)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if not formset.is_valid():
            return self.form_invalid(form)

        main_guest = form.save()

        for f in formset:
            if not f.cleaned_data:
                continue
            if f.cleaned_data.get("DELETE"):
                continue

            guest.objects.create(
                first_name=f.cleaned_data["first_name"],
                last_name=f.cleaned_data["last_name"],
                consent=main_guest.consent,
                alcohol=main_guest.alcohol,
            )

        return self.render_to_response({
            **context,
            "form": self.form_class(),
            "formset": Quiz_dop(prefix=self.formset_prefix),
            "success": True,
            "guest_name": main_guest.first_name,
        })
