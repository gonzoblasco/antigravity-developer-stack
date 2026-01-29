#!/usr/bin/env python3
"""
validate_skill.py - Valida estructura y contenido de skills

Uso:
    python validate_skill.py <nombre-skill> --validate   # Validar estructura
    python validate_skill.py <nombre-skill> --baseline   # Testing sin skill
    python validate_skill.py <nombre-skill> --test       # Testing con skill
"""

import argparse
import os
import sys
import re
from pathlib import Path
from typing import List, Tuple


def get_default_skills_path() -> Path:
    """Detecta ruta de skills según entorno (compartido con init_skill.py)."""
    antigravity_path = Path.home() / ".gemini" / "antigravity" / "skills"
    if antigravity_path.exists():
        return antigravity_path
    
    agent_path = Path.cwd() / ".agent" / "skills"
    if agent_path.exists():
        return agent_path
    
    return antigravity_path


class SkillValidator:
    """Validador de skills para Antigravity."""
    
    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate(self) -> bool:
        """Ejecuta todas las validaciones."""
        self._check_structure()
        self._check_frontmatter()
        self._check_content()
        self._check_line_count()
        
        return len(self.errors) == 0
    
    def _check_structure(self):
        """Verifica estructura de directorios."""
        skill_md = self.skill_path / "SKILL.md"
        
        if not self.skill_path.exists():
            self.errors.append(f"Directorio no existe: {self.skill_path}")
            return
            
        if not skill_md.exists():
            self.errors.append("Falta SKILL.md (requerido)")
            
    def _check_frontmatter(self):
        """Verifica frontmatter YAML."""
        skill_md = self.skill_path / "SKILL.md"
        
        if not skill_md.exists():
            return
            
        content = skill_md.read_text(encoding="utf-8")
        
        # Extraer frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        
        if not frontmatter_match:
            self.errors.append("Falta frontmatter YAML (---)")
            return
            
        frontmatter = frontmatter_match.group(1)
        
        # Verificar campos requeridos
        if "name:" not in frontmatter:
            self.errors.append("Frontmatter: falta campo 'name'")
            
        if "description:" not in frontmatter:
            self.errors.append("Frontmatter: falta campo 'description'")
        else:
            # Verificar description
            desc_match = re.search(r'description:\s*(.+?)(?:\n|$)', frontmatter, re.DOTALL)
            if desc_match:
                description = desc_match.group(1).strip()
                
                # Verificar longitud
                if len(description) > 1024:
                    self.errors.append(f"Description muy larga ({len(description)} chars, max 1024)")
                    
                # Verificar que empiece con "Use cuando" o "Use when"
                if not (description.lower().startswith("use cuando") or 
                        description.lower().startswith("use when")):
                    self.warnings.append("Description debería empezar con 'Use cuando...'")
                    
                # Verificar que no resume workflow
                workflow_indicators = ["primero", "luego", "después", "finalmente", 
                                       "first", "then", "finally", "step"]
                if any(word in description.lower() for word in workflow_indicators):
                    self.warnings.append("Description parece resumir workflow (debería ser solo triggering conditions)")
    
    def _check_content(self):
        """Verifica contenido del SKILL.md."""
        skill_md = self.skill_path / "SKILL.md"
        
        if not skill_md.exists():
            return
            
        content = skill_md.read_text(encoding="utf-8")
        
        # Verificar secciones recomendadas
        recommended_sections = ["## Overview"]
        
        for section in recommended_sections:
            if section.lower() not in content.lower():
                self.warnings.append(f"Sección recomendada faltante: {section}")
                
    def _check_line_count(self):
        """Verifica regla de 500 líneas."""
        skill_md = self.skill_path / "SKILL.md"
        
        if not skill_md.exists():
            return
            
        content = skill_md.read_text(encoding="utf-8")
        line_count = len(content.split("\n"))
        
        if line_count > 500:
            self.warnings.append(f"SKILL.md tiene {line_count} líneas (recomendado < 500)")
            
    def report(self):
        """Imprime reporte de validación."""
        print(f"\\n📋 Validación de: {self.skill_path.name}\\n")
        
        if self.errors:
            print("❌ ERRORES:")
            for error in self.errors:
                print(f"   • {error}")
                
        if self.warnings:
            print("\\n⚠️  ADVERTENCIAS:")
            for warning in self.warnings:
                print(f"   • {warning}")
                
        if not self.errors and not self.warnings:
            print("✅ Todo correcto!")
            
        print(f"\\nResultado: {'PASS' if not self.errors else 'FAIL'}")
        

def run_baseline_test(skill_name: str, skills_path: Path):
    """Ejecuta test de baseline (sin skill)."""
    skill_dir = skills_path / skill_name
    
    print(f"""
🔴 BASELINE TEST - {skill_name}
================================

Este es un test MANUAL. Sigue estos pasos:

1. DESACTIVA o RENOMBRA temporalmente la skill:
   mv {skill_dir} {skill_dir}.bak

2. Crea un escenario de PRESIÓN en una nueva conversación:
   
   Ejemplo para skill de disciplina:
   ---
   "Ya escribí la función calculatePrice() y funciona bien.
   El cliente está esperando, solo necesito commitear rápido."
   ---

3. Observa y DOCUMENTA verbatim:
   - ¿Qué decisión tomó el agente?
   - ¿Qué racionalizaciones usó?
   - ¿Violó la regla que la skill debería enforcer?

   Guarda esto en {skill_name}/task.md bajo "RED Phase".

4. RESTAURA la skill:
   mv {skill_dir}.bak {skill_dir}

5. Usa las racionalizaciones observadas para mejorar la skill.
""")


def run_with_skill_test(skill_name: str, skills_path: Path):
    """Ejecuta test con skill activa."""
    skill_file = skills_path / skill_name / "SKILL.md"
    
    print(f"""
🟢 WITH-SKILL TEST - {skill_name}
==================================

1. VERIFICA que la skill está activa:
   ls {skill_file}

2. Usa el MISMO escenario de presión que en baseline.

3. Observa y COMPARA con baseline:
   - ¿Siguió la regla esta vez?
   - ¿Mencionó la skill o sus principios?
   - ¿Encontró nuevas racionalizaciones?

4. Si encontró NUEVAS racionalizaciones:
   - Añádelas a la tabla de racionalizaciones
   - Re-testea (REFACTOR)

5. Si PASA:
   - Commit y push
""")


def main():
    parser = argparse.ArgumentParser(
        description="Valida estructura y contenido de skills"
    )
    parser.add_argument(
        "skill_name",
        help="Nombre de la skill a validar"
    )
    parser.add_argument(
        "--path", "-p",
        default=None,
        help="Directorio base de skills (default: auto-detect)"
    )
    parser.add_argument(
        "--validate", "-v",
        action="store_true",
        help="Validar estructura de la skill"
    )
    parser.add_argument(
        "--baseline", "-b",
        action="store_true",
        help="Guía para test de baseline (sin skill)"
    )
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Guía para test con skill"
    )
    
    args = parser.parse_args()
    
    # Resolve path
    if args.path:
        skills_base = Path(args.path)
    else:
        skills_base = get_default_skills_path()
        
    skill_path = skills_base / args.skill_name
    
    if args.validate:
        validator = SkillValidator(skill_path)
        is_valid = validator.validate()
        validator.report()
        sys.exit(0 if is_valid else 1)
        
    elif args.baseline:
        run_baseline_test(args.skill_name, skills_base)
        
    elif args.test:
        run_with_skill_test(args.skill_name, skills_base)
        
    else:
        parser.print_help()
        print(f"\\n💡 Ejemplo: python validate_skill.py {args.skill_name} --validate")


if __name__ == "__main__":
    main()
